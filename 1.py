from FrnkLib import *
import pycorenlp as nlp

properties = {
    "annotators": "tokenize,ssplit,pos,lemma,ner,regexner,parse,depparse,openie,coref,kbp,sentiment",
    "openie.resolve_coref": "true",
    "openie.ignore_affinity": "true"

}
url = "http://localhost:9000/"

statement = "Donald John Trump (born June 14, 1946) is the 45th and current President of the " \
            "United States, in office since January 20, 2017. Before entering politics, he wa" \
            "s a businessman and television personality. Trump was born and raised in the New" \
            " York City borough of Queens, and received an economics degree from the Wharton " \
            "School of the University of Pennsylvania. He became head of his family's real es" \
            "tate business in 1971, renamed it The Trump Organization, and expanded it to inv" \
            "olve the construction and renovation of skyscrapers, hotels, casinos, and golf c" \
            "ourses. Trump also started various side ventures, including branding and licensi" \
            "ng his name for real estate and consumer products. He managed the company until " \
            "his 2017 inauguration. Trump also gained prominence in media and entertainment, " \
            "and co-authored several books, including The Art of the Deal. He owned the Miss " \
            "Universe and Miss USA beauty pageants from 1996 to 2015 and was a producer and t" \
            "he host of the reality television game show The Apprentice from 2003 to 2015. Ac" \
            "cording to March 2018 estimates by Forbes, he is the world's 766th richest perso" \
            "n, with a net worth of US$3.1 billion. In 2000, Trump unsuccessfully campaigned " \
            "for the Reform Party nomination for president. In 2015 he entered the 2016 presi" \
            "dential race as a Republican. He defeated sixteen opponents in the primaries. Co" \
            "mmentators described his political positions as populist, protectionist, and nat" \
            "ionalist. His campaign received extensive free media coverage; many of his publi" \
            "c statements were controversial or false. Trump was elected president against De" \
            "mocratic nominee Hillary Clinton; his victory upset the expectations of polls an" \
            "d analysts. He became the oldest and wealthiest person ever to assume the presid" \
            "ency, the first without prior military or government service, and the fifth to h" \
            "ave won the election while losing the popular vote. His election and policies ha" \
            "ve sparked numerous protests. In domestic policy, Trump appointed Neil Gorsuch t" \
            "o the Supreme Court. Citing security concerns, he ordered a travel ban on citize" \
            "ns from several Muslim-majority countries; a revised version of the ban was impl" \
            "emented after legal challenges. He signed tax reform legislation that cut rates " \
            "and eliminated the Affordable Care Act insurance mandate. In foreign policy, Tru" \
            "mp withdrew the United States from the Paris Agreement on climate change, partia" \
            "lly reversed the Cuban thaw, and ordered missile strikes in Syria after chemical" \
            " weapon attacks. He accepted an invitation from North Korean leader Kim Jong-un " \
            "for direct talks regarding the latter's nuclear weapons program, recognized Jeru" \
            "salem as the capital of Israel, and withdrew the United States from the Iran nuc" \
            "lear deal. After Trump dismissed FBI Director James Comey in 2017, the Justice D" \
            "epartment appointed Robert Mueller as special counsel in an investigation into c" \
            "oordination or links between the Trump campaign and Russian government in connec" \
            "tion with Russian interference in the 2016 elections, and related matters. Trump" \
            " has repeatedly denied any such collusion."

# statement = "Donald Trump was running for the President of the United States of America. " \
#             "He is 71 years old. " \
#             "He won the election in December"
# print(statement)

# exit(0)

# statement = "Donald Trump is the President of USA. He is the dumbest person alive. " \
#             "His daughter is Ivanka and she is hot."

# statement="A equals B. B equals C"
# statement = "Donald Trump is President of the United States of America"

# statement = "Alex visited Greece, India and USA in 2012. " \
#             "His favourite country was Greece. " \
#             "He is currently visiting Singapore. " \
#             "India was the worst country"



# statement = "In early 2013, he left Bridgewater to become a Senior Research Scholar and " \
#             "Hertog Fellow on National Security Law at Columbia Law School."


s_nlp = nlp.StanfordCoreNLP(url)

dx, _ = get_decomposition(statement, s_nlp)
decompositions = [dx]
decomposed_statements = set()
for decomposition in decompositions:
    for ddx in decomposition:
        extracted_information = ddx['openie']
        for info in extracted_information:
            print(info['subject'], info['relation'], info['object'], sep='|')
            decomposed_statements.add(sentence_from_info(info))

#     dx = decompose(decomposition)
#     for d in dx:
#         sx = d[0]
#         if sx not in decomposed_statements:
#             decomposed_statements += [sx]
# #         if sx not in processed_statements:
#             processed_statements += [sx]
#             ddx, _ = get_decomposition(sx, s_nlp)
#             decompositions += [ddx]
#             for x in ddx[0]['openie']:
#                 dsx = sentence_from_info(x)
#                 if dsx not in processed_statements:
#                     print(dsx, 'XXXXX', x['subject'], '|', x['relation'], '|', x['object'])

decomposed_statements = sorted(decomposed_statements)
tree_feed = []
for ds in decomposed_statements:
    tree_feed += [[WordNode(i) for i in ds.split(" ")]]
# ddx = get_decomposition(i, s_nlp)[0]
# print(decompose(ddx))


node = build_tree(tree_feed)
# print(node)
final_set = []
for n in node.nextNodes:
    final_set += decompose_tree(n)

final_txt = '. '.join(final_set)

# print(final_txt)

out = get_decomposition(statement, s_nlp)[0]

print(out)

for i in out:
    tokens = [x['word'] for x in i['tokens']]
    lemmas = [x['lemma'] for x in i['tokens']]
    ners = [(x['ner'], x['text']) for x in i['entitymentions']]
    print(tokens)
    print(clean_stopwords(tokens))
    print(lemmas)
    print(ners)
