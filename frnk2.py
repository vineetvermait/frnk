from FrnkLib import *
import json

# data = "Donald Trump won the presidential elections in 2016. He became the President in 2017"
data = "Alex Mathews loves Martha. Martha loves Jake. Jake loves Alex"
# data = "Alex saw a saw. It was made of metal"
print(data)
snlp = nlp.StanfordCoreNLP(url)
response = snlp.annotate(data, properties)
response = json.loads(response)

corefs = response['corefs']
sentences = response['sentences']


def find_from_tokens(_tokens, _offset_start_index, _offset_end_index):
    tokens_to_return = []
    for _token in _tokens:
        if _token["characterOffsetBegin"] >= _offset_start_index and _token["characterOffsetEnd"] <= _offset_end_index:
            tokens_to_return += [_token]
    return tokens_to_return


def find_tokens_from_corefs(_corefs, _tokens):
    pass
    # for _ref in _corefs:
    #     if _ref["startIndex"] == _offset_start_index and _ref["endIndex"] == _offset_end_index:
    #         return _token


print("Tokens")
for sentence in sentences:
    print(json.dumps(sentence['tokens']))

print("OpenIE")
infos = []
for sentence in sentences:
    infos += sentence['openie']

print(json.dumps(infos))

print("Entities ")
entities = []
for sentence in sentences:
    tokens = sentence['tokens']
    for entity in sentence['entitymentions']:
        # _entity = filter_keys(entity, ["text", "ner"])
        entity_tokens = find_from_tokens(tokens, entity["characterOffsetBegin"], entity["characterOffsetEnd"])
        print("->", entity_tokens)
        # entx = filter_keys(token, ['word', 'originalText', 'lemma', 'pos', 'ner', 'speaker'])
        entities += [entity]
        # print("--->", filter_keys(entity, ["text", "ner"]))
        # print(build_attr_map(_entity))
        # print(build_attr_map(entx))
print(json.dumps(entities))
