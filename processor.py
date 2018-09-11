from FrnkLib import *
import json


def find_from_tokens(_tokens, _offset_start_index, _offset_end_index):
    tokens_to_return = []
    for _token in _tokens:
        if _token["characterOffsetBegin"] >= _offset_start_index and _token["characterOffsetEnd"] <= _offset_end_index:
            tokens_to_return += [_token]
    return tokens_to_return


data = "Alex loves Martha. Martha loves Jake. Jake hates Alex"
print(data)
snlp = nlp.StanfordCoreNLP(url)
response = snlp.annotate(data, properties)
response = json.loads(response)
corefs = response['corefs']
sentences = response['sentences']

print(json.dumps(corefs))
# Find all entities
primary_entities = []
tokens = []
# ['index',
# 'basicDependencies',
# 'enhancedDependencies',
# 'enhancedPlusPlusDependencies',
# 'openie',
# 'entitymentions',
# 'tokens']

for i, sentence in enumerate(sentences):
    for entity in sentence['entitymentions']:
        entity['sentNum'] = i + 1
        primary_entities += [entity]
print(json.dumps(primary_entities))
# Map entities to tokens and get meta data
for i, sentence in enumerate(sentences):
    for token in sentence['tokens']:
        token['sentNum'] = i + 1
        token['sentToken'] = token["index"] - 1
        tokens += [token]
print(json.dumps(tokens))
print("-------------")
for entity in primary_entities:
    for token in tokens:
        if (token['sentNum'] == entity['sentNum']
                and
                entity['tokenBegin'] <= token['sentToken'] < entity['tokenEnd']):
            print(filter_keys(entity, ['text', 'ner']),
                  filter_keys(token, ['word', 'originalText', 'lemma', 'pos', 'speaker']))
            if 'tokens' not in entity:
                entity['tokens'] = []
            entity['tokens'] += [filter_keys(token,
                                             ['index', 'sentToken', 'word', 'originalText', 'lemma', 'pos',
                                              'speaker'])]
print(json.dumps(primary_entities))
# Map and reduce tokens from co-refs
# Create relations between entities using open ie
# Serialize data to Graph DB
