from FrnkLib import *

txt = "The United Nations Educational, Scientific and Cultural Orga" \
      "nisation is a specialized agency of the United Nations (UN) based in Paris. Its decla" \
      " red purpose is to contribute to peace and security by promot" \
      "ing international collaboration through educational, scienti" \
      "fic, and cultural reforms in order to increase universal res" \
      "pect for justice, the rule of law, and human rights along wi" \
      "th fundamental freedom proclaimed in the United Nations Char" \
      "ter. It is the successor of the League of Nations' Intern" \
      "ational Committee on Intellectual Cooperation. UNESCO has 19" \
      "5 member states and ten associate members. Most of " \
      "its field offices are \"cluster\" offices covering three or mo" \
      "re countries; national and regional offices also exist. UNES" \
      "CO pursues its objectives through five major programs: educa" \
      "tion, natural sciences, social/human sciences, culture and c" \
      "ommunication/information. Projects sponsored by UNESCO inclu" \
      "de literacy, technical, and teacher-training programs, inter" \
      "national science programs, the promotion of independent medi" \
      "a and freedom of the press, regional and cultural history pr" \
      "ojects, the promotion of cultural diversity, translations of" \
      " world literature, international cooperation agreements to s" \
      " ecure the world's cultural and natural heritage (World Herit" \
      "age Sites) and to preserve human rights, and attempts to bri" \
      "dge the worldwide digital divide. It is also a member of the" \
      " United Nations Development Group. UNESCO's aim is \"to co" \
      " ntribute to the building of peace, the eradication of povert" \
      "y, sustainable development and intercultural dialogue throug" \
      "h education, the sciences, culture, communication and inform" \
      "ation\". Other priorities of the organization include atta" \
      "ining quality Education For All and lifelong learning, addre" \
      "ssing emerging social and ethical challenges, fostering cult" \
      "ural diversity, a culture of peace and building inclusive kn" \
      "owledge societies through information and communication. " \
      "The broad goals and objectives of the international communit" \
      "y—as set out in the internationally agreed development goals" \
      ", including the Millennium Development Goals (MDGs)—underpin" \
      " all UNESCO strategies and activities."
print(txt)

response = snlp.annotate(txt, properties)
response = json.loads(response)
sentences = response['sentences']


def n_gram_stats(sents, _n=2, top=10):
    _sx = 0
    _grid = {}
    for _i in sents:
        tokens = [_z['word'] for _z in _i['tokens']]
        tokens = clean_stopwords(tokens)
        for n in range(0, len(tokens) - _n):
            token_set = tuple([t for t in tokens[n:n + _n]])

            if token_set not in _grid:
                _grid[token_set] = 0
            _grid[token_set] = _grid[token_set] + 1

            _sx += 1
    data = sorted([(' '.join(_i), (_grid[_i] / (_sx / _n)) * 100) for _i in _grid], reverse=True, key=lambda x: x[1])
    return _sx, data[:top]


for _nx in range(1, 10):
    sx, dx = n_gram_stats(sentences, _nx)

    # print(sx)
    for i in dx:
        print(i[0], "\t", i[1])
    print()


"".replace()