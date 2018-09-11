from FrnkLib import *

statement = "Alex saw Bob"
s_nlp = nlp.StanfordCoreNLP(url)

# statement = "Justice Department appointed Robert Mueller as special counsel in investigation into " \
#             "coordination between Trump campaign in connection with Russian interference in 2016 elections"

# data = breakdown(statement, s_nlp)
# data = sorted(data)
# for i in data:
#     ddx = get_decomposition(i, s_nlp)[0][0]
#     for ii in ddx['openie']:
#         print(ii['subject'], '|', ii['relation'], '|', ii['object'])

ddx = get_decomposition(statement, s_nlp)[0]
print(ddx)
