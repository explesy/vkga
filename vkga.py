#!/usr/bin/python3

import urllib.request
import json
import webbrowser
from string import Template


# We get massive of bytes, so we read it and decode to utf-8 
data = urllib.request.urlopen('https://api.vk.com/method/wall.get?domain=trap_edm&count=10').read().decode('utf-8')
# Convert data from JSON to Python
data_encoded = json.loads(data)

print("DATA: {}".format(type(data_encoded)))
print("RESPONSE: {}".format(type(data_encoded['response'])))
print("RESPONSE ###: {}".format(type(data_encoded['response'][2])))
print("LIKES: {}".format(type(data_encoded['response'][2]['likes'])))
print("COUNTS: {}".format(type(data_encoded['response'][2]['likes']['count'])))


list_of_posts = data_encoded['response'][1:]

# print("LIST OF POSTS: {}".format(type(list_of_posts)))
# print(list_of_posts[0]['likes'])


list_of_posts = sorted(list_of_posts, key=lambda k: k['likes']['count'], reverse = True) 


# for item in data_encoded['response'][1:]:
# 	print("=========================================")
# 	print("ITEM: {}".format(type(item)))
# 	print(item['likes'])


# print(data_encoded['response'][2]['likes']['count'])

# print(data_encoded['response'][1]['text'])

# data_sorted = sorted(data_encoded['response'][2])

# print(data_sorted)

result = ""

for i in range(0, 10):
	result += "<h1>"
	result += str(list_of_posts[i]['likes']['count'])
	result += "</h1>=====</br>"
	result += " --> "
	result += str(list_of_posts[i]['text'])
	result += "</br></br>"

# 	print(result)


with open('index.tpl', 'r') as tpl:
		template_raw = tpl.read()

page = Template(template_raw)
page = page.substitute(insert_data=result) #Exactly page = in other way we get Template object, not a string

# print(page)

with open('index.html', 'w') as html:
		html.write(page)

webbrowser.open("./index.html")