from FrnkLib import *

properties = {
    "annotators": "tokenize,ssplit,pos,lemma,ner,regexner,parse,depparse,openie,coref,kbp,sentiment",
    "openie.resolve_coref": "true",
    "openie.ignore_affinity": "true"

}
url = "http://localhost:9000/"  # + urllib.parse.quote_plus(json.dumps(properties))

data = "Donald Trump is the President of USA. He is the dumbest person alive. His daughter is Ivanka and she is hot."

data = "Donald Trump is President"


# class ExtractedInformation:
#     def __init__(self, information, span, tokens):
#         self.info = information
#         self.span = span
#         self.tokens = tokens
#
#     def __str__(self):
#         return self.info


def get_decomposition(statement, nlp):
    props = {
        "annotators": "tokenize,openie,coref",
        "openie.resolve_coref": "true",
        "openie.ignore_affinity": "true"
    }

    response = nlp.annotate(statement, props)
    response = json.loads(response)
    sentences = response['sentences']
    return sentences, response


def find_tokens_from_spans(_info, token_list):
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

    return _info


def get_infos(statements, ie_set):
    for statement in statements:
        token_list = statement['tokens']

        for _info in statement['openie']:

            _info = find_tokens_from_spans(_info, token_list)

            subject = _info['subject']
            relation = _info['relation']
            obj = _info['object']

            _ie = subject + ' ' + relation + ' ' + obj
            _ie = _ie.replace("_", ' ')
            if _ie not in ie_set:
                ie_set += [_ie]
    # _subject.tokens + _relation.tokens + _obj.tokens
    return


def decompose(_nlp, sentence):
    ies = []
    ies_tokens = []
    sentences, ddx = get_decomposition(sentence, _nlp)
    ies_tokens += [get_infos(sentences, ies)]
    ies = sorted(ies)

    for ie in ies:
        sentences, _ = get_decomposition(ie, _nlp)
        get_infos(sentences, ies)
        ies_tokens += [get_infos(sentences, ies)]
    return ies, ies_tokens


s_nlp = nlp.StanfordCoreNLP(url)

info, token_sets = decompose(s_nlp, data)

for i in info:
    print(i)
#
# for i in token_sets:
#     print(i)

data_set = [[WordNode(n) for n in sent] for sent in token_sets]
neo = NeoConnect()
node = build_tree(data_set)
# print('--->', node)
node.current = {'word': node.current}
qry_set, nx = create_nodes(node)
neo.db_connect('MATCH (n) detach delete n')
for i in qry_set:
    print(i)
    neo.db_connect(i)
