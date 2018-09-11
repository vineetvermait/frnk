# from FrnkLib import *
#
# _data_set = [['Bridgewater', 'become', 'Senior', 'Research', 'Scholar'],
#              ['Bridgewater', 'become', 'Senior', 'Research', 'Scholar', 'at', 'Columbia', 'Law', 'School'],
#              ['Bridgewater', 'become', 'Senior', 'Research', 'Scholar', 'on', 'National', 'Security', 'Law'],
#              ['Bridgewater', 'become', 'Senior', 'Research', 'Scholar', 'on', 'National', 'Security', 'Law', 'at',
#               'Columbia', 'Law', 'School']]
#
# # _data_set += [['James', 'Brien', 'Comey', 'Jr.', 'became', 'counsel'],
# #               ['James', 'Brien', 'Comey', 'Jr.', 'became', 'counsel', 'at', 'Bridgewater', 'Associates'],
# #               ['James', 'Brien', 'Comey', 'Jr.', 'became', 'counsel', 'at', 'Bridgewater', 'Associates', 'based'],
# #               ['James', 'Brien', 'Comey', 'Jr.', 'became', 'counsel', 'at', 'Bridgewater', 'Associates', 'based',
# #                'in', 'Westport']]
#
# data_set = [[WordNode(n) for n in sent] for sent in _data_set]
# out_set = []
#
# node = build_tree(data_set[:])
#
# # print(node)
#
#
# for n in node.nextNodes:
#     print(decompose_tree(n))

# import urllib.request, urllib.parse
#
# auth_api_endpoint = "https://api.automation.exterionmedia.com/auth/key/auth_token"
# system_user_key = "92087A911494455885C6A683C61468F9"
# # data = urllib.parse.urlencode({"Authorization": system_user_key}).encode()
# # req = urllib.request.Request(auth_api_endpoint,
# #                              data=data,
# #                              # headers={"Content-Type": "application/x-www-form-urlencoded"},
# #                              method="POST")
# # response = urllib.request.urlopen(req).read().decode()
#
# values = {"Authorization": system_user_key}
#
# data = urllib.parse.urlencode(values)
# data = data.encode('ascii')
#
# req = urllib.request.Request(auth_api_endpoint, data)
#
# with urllib.request.urlopen(req) as response:
#     the_page = response.read()
#     print(the_page)


import wikipedia

page = wikipedia.page("British Petroleum")
# print(dir(page))
# 'categories', 'content', 'coordinates', 'html',
# 'images', 'links', 'original_title', 'pageid', 'parent_id',
# 'references', 'revision_id', 'section', 'sections', 'summary', 'title', 'url'

# print(page.categories)
# print(page.content)
# print(page.images)
# print(page.links)
# print(page.original_title)
# print(page.parent_id)
print(page.sections)
print(page.section())
print(dir(page.section))
# print(page.references)
