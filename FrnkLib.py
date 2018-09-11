from nltk.corpus import stopwords

from neo4j.v1 import GraphDatabase
import re
from Node import Node
import pycorenlp as nlp
import json


def clean_stopwords(txt):
    _stopwords = set(stopwords.words('english'))  #

    for i in [",", "\"", "'", "`", "'s", ";"]:
        _stopwords.add(i)

    final_txt = txt
    if len(txt) > 1:
        final_txt = [x for x in txt if x not in _stopwords]
    return final_txt


def convert(word):
    break_down = [x for x in re.split(r"\W+", word)]
    words = clean_stopwords(break_down)
    ret_val = ''.join(x.capitalize() or '_' for x in words)
    return ret_val


properties = {
    "annotators": "tokenize,ssplit,pos,ner,depparse,openie,coref",
    "openie.resolve_coref": "true",
    "openie.ignore_affinity": "true"
}
url = "http://localhost:9000/"  # + urllib.parse.quote_plus(json.dumps(properties))
snlp = nlp.StanfordCoreNLP(url)


class NeoConnect:
    def __init__(self):
        pass

    neo4j_uri = "bolt://localhost:7687"
    user, password = ("neo4j", "admin")

    _driver = GraphDatabase.driver(neo4j_uri, auth=(user, password))

    def db_connect(self, query):
        self._driver = GraphDatabase.driver(self.neo4j_uri, auth=(self.user, self.password))
        response = self.execute(query)
        self._driver.close()
        return response

    def txn_to_execute(self, tx, query):
        result = tx.run(query)
        return result

    def execute(self, qry):
        with self._driver.session() as session:
            _response = session.write_transaction(self.txn_to_execute, qry)

            return [{x: i[x] for x in i.keys()} for i in _response]


def build_attr_map(_obj):
    obj_str = '{'
    for prop in _obj:
        val = _obj[prop]
        obj_str += prop + ':"' + str(val).lower() + '", '
    obj_str = obj_str[:-2]
    obj_str += '}'
    return obj_str


def create_entity_query(entity):
    obj_str = 'MERGE (a:TOKEN' + (':' + entity['ner'] if entity['ner'] != 'O' else '') + build_attr_map(entity) + ')'
    return obj_str


def find_tokens(tokens, span_start, span_end, information):
    required_info = ['word', 'originalText', 'lemma', 'pos', 'ner', 'speaker']
    extracted_tokens = []
    for span in range(span_start, span_end):
        if re.search(tokens[span]['word'], information) is not None:
            token = {k: tokens[span][k] for k in required_info}
            extracted_tokens += [token]
    return extracted_tokens


class WordNode:
    def __init__(self, current):
        self.current = current
        self.nextNodes = []

    def __str__(self):
        return '{' + str(self.current) + ': [' + (', '.join([str(node) for node in self.nextNodes])) + '] }'


def build_tree(ds):
    start_node = WordNode('X')
    for i in ds:
        i.insert(0, start_node)

    for data in ds:
        current_node = start_node
        for iz, node in enumerate(data):
            if current_node.current != node.current:
                key_list = [ix.current for ix in current_node.nextNodes]
                indx = key_list.index(node.current) if node.current in key_list else -1
                if node.current not in [ix.current for ix in current_node.nextNodes]:
                    current_node.nextNodes += [node]
                else:
                    node = current_node.nextNodes[indx]

            current_node = node
    return start_node


def create_nodes(_node):
    qry_set = []
    nx = Node(['NODE'], _node.current)
    qry = 'MERGE ' + nx.build_node_query('s')
    qry_set += [qry]
    for nextNode in _node.nextNodes:
        _qry_set, _chld_nx = create_nodes(nextNode)
        qry_set += _qry_set
        qry_set += [
            'MATCH ' + nx.build_node_query('p') + ',' + _chld_nx.build_node_query('c') + ' MERGE (p)-[r:_]->(c)']
    # qry_set += ['MERGE(w:NODE {word:"' + node.current + '"})']
    # print(_node, file=sys.stderr)
    # print(qry, file=sys.stderr)

    return qry_set, nx


def decompose_tree(_node):
    variations = []
    for _nextNode in _node.nextNodes:
        variations += decompose_tree(_nextNode)

    return [_node.current + ' ' + i for i in variations] if len(variations) > 0 else [_node.current]


def decompose(_decomposition):
    extracted_info_set = []
    extracted_info_tokens = []
    for d in _decomposition:
        token_list = d['tokens']
        for ie in d['openie']:
            inject_tokens_from_spans(ie, token_list)
            sent = sentence_from_info(ie)
            extracted_info_set += [sent]
            extracted_info_tokens += [ie['subject_tokens'] + ie['relation_tokens'] + ie['obj_tokens']]
        extracted_info_set = sorted(extracted_info_set)
    return [(s, t) for s, t in zip(extracted_info_set, extracted_info_tokens)]


def get_decomposition(_statement, nlp):
    props = {
        "annotators": "tokenize,ssplit,pos,lemma,ner,regexner,parse,depparse,openie,coref,kbp,sentiment",
        "openie.resolve_coref": "true",
        "openie.ignore_affinity": "true"
    }

    response = nlp.annotate(_statement, props)
    response = json.loads(response)
    sentences = response['sentences']
    return sentences, response


def inject_tokens_from_spans(_info, token_list):
    _subject = _info['subject']
    _relation = _info['relation']
    _obj = _info['object']

    subject_r_start, subject_r_end = _info['subjectSpan']
    relation_r_start, relation_r_end = _info['relationSpan']
    obj_r_start, obj_r_end = _info['objectSpan']

    subject_tokens = find_tokens(token_list, subject_r_start, subject_r_end, _subject)
    relation_tokens = find_tokens(token_list, relation_r_start, relation_r_end, _relation)
    obj_tokens = find_tokens(token_list, obj_r_start, obj_r_end, _obj)

    _info['subject_tokens'] = subject_tokens
    _info['relation_tokens'] = relation_tokens
    _info['obj_tokens'] = obj_tokens


def sentence_from_info(_info):
    _subject = _info['subject']
    _relation = _info['relation']
    _obj = _info['object']
    _ie = _subject + ' ' + _relation + ' ' + _obj
    _ie = _ie.replace("_", ' ')

    return _ie


def breakdown(_information, _nlp, processed=set()):
    _xd, _ = get_decomposition(_information, _nlp)

    for _xdd in _xd:
        for info in _xdd['openie']:
            sx = sentence_from_info(info)
            if sx not in processed:
                processed.add(sx)
                breakdown(sx, _nlp, processed)
    return processed


def filter_keys(_data, _keys):
    _dx = {}
    for _key in _keys:
        _dx[_key] = _data[_key]
    return _dx
