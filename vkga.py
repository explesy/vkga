#!/usr/bin/python3

import urllib.request
import json
import webbrowser
from string import Template
import argparse

def get_post_list(group, number_of_posts):
	''' Return sorted by likes list of posts from the wall of community '''

	url = "https://api.vk.com/method/wall.get?domain={}&count={}".format(group, number_of_posts)
	# We get massive of bytes, so we read it and decode to utf-8 
	data = urllib.request.urlopen(url).read().decode('utf-8')
	# Convert data from JSON to Python
	data_encoded = json.loads(data)


	list_of_posts = data_encoded['response'][1:]

	list_of_posts = sorted(list_of_posts, key=lambda k: k['likes']['count'], reverse = True) 

	return list_of_posts


def html_gen(list_of_posts, number_of_posts):
	''' Generate resulting html file with obtained data '''

	result = ""

	for i in range(0, number_of_posts):
		result += "<h1>"
		result += str(list_of_posts[i]['likes']['count'])
		result += "</h1>=====</br>"
		result += str(list_of_posts[i]['text'])
		result += "</br>"
		if 'attachments' in list_of_posts[i]:
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
				elif list_of_posts[i]['attachments'][j]['type'] == 'video':
					result += "<b>Video: </b>"
					result += "</br>"
					result += str(list_of_posts[i]['attachments'][j]['video']['title'])
					result += "</br>"
					result += "<img src=\""
					result += str(list_of_posts[i]['attachments'][j]["video"]['image_big'])
					result += "\" />"
					result += "</br>"
		result += "</br></br>"
		
	with open('index.tpl', 'r') as tpl:
			template_raw = tpl.read()

	page = Template(template_raw)
	page = page.substitute(insert_data=result) #Exactly page = in other way we get Template object, not a string

	#Important. Without parametr encoding='utf-8' don't working under Windows
	with open('index.html', 'w', encoding='utf-8') as html:
			html.write(page)

	webbrowser.open("index.html")


def main():
	parser = argparse.ArgumentParser(description='Analyze group in vk and return list of most popular posts ordered by the number of likes')
	parser.add_argument("-g", "--group", help="choose group to analyze", type=str, default='trap_edm', metavar='vk_domain')
	parser.add_argument("-c", "--count", help="number of posts from the wall to analyze, integer in range 0..100", type=int, choices=range(101), default=10, metavar='[0..100]')
	args = parser.parse_args()

	list = get_post_list(args.group, args.count)
	html_gen(list, args.count)


main()
