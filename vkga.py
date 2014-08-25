#!/usr/bin/python3

import urllib.request
import json
import webbrowser
from string import Template

number_of_posts = 100
group = "e_music"


url = "https://api.vk.com/method/wall.get?domain={}&count={}".format(group, number_of_posts)
# We get massive of bytes, so we read it and decode to utf-8 
data = urllib.request.urlopen(url).read().decode('utf-8')
# Convert data from JSON to Python
data_encoded = json.loads(data)


list_of_posts = data_encoded['response'][1:]

list_of_posts = sorted(list_of_posts, key=lambda k: k['likes']['count'], reverse = True) 


result = ""

for i in range(0, number_of_posts):
	result += "<h1>"
	result += str(list_of_posts[i]['likes']['count'])
	result += "</h1>=====</br>"
	# result += " --> "
	result += str(list_of_posts[i]['text'])
	result += "</br>"
	for j in range(0, len(list_of_posts[i]['attachments'])):
		if list_of_posts[i]['attachments'][j]['type'] == 'photo':
			result += "<img src=\""
			result += str(list_of_posts[i]['attachments'][j]["photo"]['src'])
			result += "\" />"
			result += "</br>"
		elif list_of_posts[i]['attachments'][j]['type'] == 'audio':
			result += "<a href=\""
			result += str(list_of_posts[i]['attachments'][j]['audio']['url'])
			result += "\">"
			result += str(list_of_posts[i]['attachments'][j]['audio']['artist']) + " - " + str(list_of_posts[i]['attachments'][j]['audio']['title'])
			result += "</a>"
			result += "</br>"
	result += "</br></br>"
	

with open('index.tpl', 'r') as tpl:
		template_raw = tpl.read()

page = Template(template_raw)
page = page.substitute(insert_data=result) #Exactly page = in other way we get Template object, not a string

with open('index.html', 'w') as html:
		html.write(page)

webbrowser.open("./index.html")