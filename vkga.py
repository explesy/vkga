#!/usr/bin/python3

import urllib.request
import json
import webbrowser
from string import Template
import argparse

class PostList:

	def __init__(self, domain, number_of_posts):
		'''
		self.domain 			- domain of target
		self.number_of_posts	- amount of posts to get from the wall
		self.posts 				- list of posts
		'''

		self.domain = domain
		self.number_of_posts = number_of_posts

		url = "https://api.vk.com/method/wall.get?domain={}&count={}".format(domain, number_of_posts)
		# We get massive of bytes, so we read it and decode to utf-8 
		data = urllib.request.urlopen(url).read().decode('utf-8')
		# Convert data from JSON to Python
		data_encoded = json.loads(data)

		list_of_posts = data_encoded['response'][1:]

		self.posts = list_of_posts

	def likes_sort(self):
		''' Sort by likes list of posts from the wall '''

		self.posts = sorted(self.posts, key=lambda k: k['likes']['count'], reverse = True) 


	def html_gen(self):
		''' Generate resulting html file with obtained data '''

		result = ""

		for i in range(0, self.number_of_posts):
			result += "<h1>"
			result += str(self.posts[i]['likes']['count'])
			result += "</h1>=====</br>"
			result += str(self.posts[i]['text'])
			result += "</br>"
			if 'attachments' in self.posts[i]:
				for j in range(0, len(self.posts[i]['attachments'])):
					if self.posts[i]['attachments'][j]['type'] == 'photo':
						result += "<img src=\""
						result += str(self.posts[i]['attachments'][j]["photo"]['src'])
						result += "\" />"
						result += "</br>"
					elif self.posts[i]['attachments'][j]['type'] == 'audio':
						result += "<a href=\""
						result += str(self.posts[i]['attachments'][j]['audio']['url'])
						result += "\">"
						result += str(self.posts[i]['attachments'][j]['audio']['artist']) + " - " + str(self.posts[i]['attachments'][j]['audio']['title'])
						result += "</a>"
						result += "</br>"
					elif self.posts[i]['attachments'][j]['type'] == 'video':
						# result += "<b>Video: </b>"
						# result += "</br>"
						result += str(self.posts[i]['attachments'][j]['video']['title'])
						result += "</br>"
						result += "<img src=\""
						result += str(self.posts[i]['attachments'][j]["video"]['image_big'])
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
	parser = argparse.ArgumentParser(description='Analyze group or user in vk and return list of most popular posts ordered by the number of likes')
	parser.add_argument("-d", "--domain", help="choose group or user to analyze", type=str, default='trap_edm', metavar='vk_domain')
	parser.add_argument("-c", "--count", help="number of posts from the wall to analyze, integer in range 0..100", type=int, choices=range(101), default=10, metavar='[0..100]')
	args = parser.parse_args()

	list = PostList(args.domain, args.count)
	list.likes_sort()
	list.html_gen()


if __name__ == '__main__':
  main()