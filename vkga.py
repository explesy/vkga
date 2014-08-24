#!/usr/bin/python3

import urllib.request
import json


# We get massive of bytes, so we read it and decode to utf-8 
data = urllib.request.urlopen('https://api.vk.com/method/wall.get?domain=trap_edm').read().decode('utf-8')
# Convert data from JSON to Python
data_encoded = json.loads(data)

print(data_encoded['response'][2]['likes']['count'])