from FrnkLib import *
import sys

data = "Donald Trump won the presidential elections in 2016. He became the President in 2017"
data = "Alex loves Martha. Martha loves Jake."
# data = "Donald Trump is the President of the United States of America. He is 71 years old."

# data = "Donald Trump is the President of USA. He is the dumbest person alive. His daughter is Ivanka " \
#        "and she is the advisor to the president."

# data = "Alex visited Greece, India and USA in 2012. " \
#        "His favourite country was Greece. " \
#        "He is currently visiting Singapore"
# data = "Alex country was Greece. " \
#        "Alex favourite country was Greece. " \
#        "Alex is currently visiting Singapore. " \
#        "Alex is visiting Singapore. " \
#        "Alex visited Greece in 2012. " \
#        "Alex visited India in 2012. " \
#        "Alex visited USA in 2012"
#
# data = "Alex country was Greece. " \
#        "Alex visited India in 2012. " \
#        "India was country. " \
#        "India was worst country. " \
#        "Alex visited USA in 2012. " \
#        "Alex favourite country was Greece. " \
#        "Alex is currently visiting Singapore. " \
#        "Alex is visiting Singapore. " \
#        "Alex visited Greece in 2012. " \
#        ""
# data = "Bob loves Martha. Martha loves Bob"

print(data)
snlp = nlp.StanfordCoreNLP(url)

response = snlp.annotate(data, properties)
response = json.loads(response)
sentences = response['sentences']

trace_map = {}
word_map = {}
root_point = 0

neo = NeoConnect()
qry_string = ['MATCH (n) DETACH DELETE n']
# qry_string = []
for sentence in sentences:
    word_map = []

    token_list = sentence['tokens']

    for info in sentence['openie']:
        try:
            subject = info['subject']
            relation = info['relation']
            obj = info['object']

            subject_r_start, subject_r_end = info['subjectSpan']
            relation_r_start, relation_r_end = info['relationSpan']
            object_r_start, object_r_end = info['objectSpan']

            subject_items = token_list[subject_r_start:subject_r_end]
            relation_items = token_list[relation_r_start:relation_r_end]
            object_items = token_list[object_r_start:object_r_end]

            print(subject, relation, obj)

            subject_tokens = find_tokens(token_list, subject_r_start, subject_r_end, subject)
            relation_tokens = find_tokens(token_list, relation_r_start, relation_r_end, relation)
            obj_tokens = find_tokens(token_list, object_r_start, object_r_end, obj)

            qries = ['MERGE (a:SUBJECT {word:"' + subject.lower() + '"})',
                     'MERGE (b:OBJ {word:"' + obj.lower() + '"})',
                     'MATCH (a:SUBJECT ), (b:OBJ ) where a.word="'
                     + subject.lower()
                     + '" and b.word="'
                     + obj.lower()
                     + '" merge (a)-[c:' + convert(relation) + ']->(b)']

            qry_string += [q for q in qries if q not in qry_string]

            if len(subject_tokens) == 1:
                for i in subject_tokens:
                    i['word'] = i['word'].lower()
                    qry_string += ['MATCH (sub:SUBJECT {word:"' + subject.lower() + '"}) set ' + ', '.join(
                        ['sub.' + _i + '="' + i[_i] + '"' for _i in i if _i != 'word']) + ', sub:TOKEN' + (
                                       ', sub:' + i['ner'] if i['ner'] != 'O' else '')]
            else:
                for i in subject_tokens:
                    i['word'] = i['word'].lower()
                    qry_string += [create_entity_query(i)]
                    qry_string += ['MATCH (sub:SUBJECT), (tok:TOKEN ) WHERE sub.word="' + subject.lower()
                                   + '" and tok.word="' + i["word"] + '" MERGE (sub)-[c:_ {txn:1234}]->(tok)']

            if len(obj_tokens) == 1:
                for i in obj_tokens:
                    i['word'] = i['word'].lower()
                    qry_string += ['MATCH (obj:OBJ {word:"' + obj.lower() + '"}) set ' + ', '.join(
                        ['obj.' + _i + '="' + i[_i] + '"' for _i in i if _i != 'word']) + ', obj:TOKEN' + (
                                       ', obj:' + i['ner'] if i['ner'] != 'O' else '')]
            else:
                for i in obj_tokens:
                    i['word'] = i['word'].lower()
                    qry_string += [create_entity_query(i)]
                    qry_string += [
                        'MATCH (obj:OBJ), (tok:TOKEN ) WHERE obj.word="' + obj.lower() +
                        '" and tok.word="' + i["word"] + '" MERGE (obj)-[c:_]->(tok)']

        except:
            print("Error!!!", info)
            print("Unexpected error:", sys.exc_info())

for i in qry_string:
    try:
        print(i)
        neo.db_connect(i)
    except:
        print("Unexpected error:", sys.exc_info())
        print("skipping: ", i)

# for refs in response['corefs']:
#     print('-----------------------')
#     ref = response['corefs'][refs]
#     # print(ref)
#     for r in ref:
#         # for i in r:
#         #     print(i, ':', r[i])
#         # print()
#         print(r)
#     print('-----------------------')
