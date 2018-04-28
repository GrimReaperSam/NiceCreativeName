# coding=UTF-8

import os
import requests

for root, dirs, files in os.walk('LandNumber/'):
	for file in files:
		json_file = os.path.splitext(file)[0] + '.json'
		json_file_path = 'GeoJson/' + json_file
		if os.path.exists(json_file_path):
			continue

		url = 'http://twland.ronny.tw/index/search?'

		csv_file = open('LandNumber/' + file, 'r', encoding='utf-8')
		print("[Dealing] " + file)
		for line in csv_file.readlines():
			url += 'lands[]=臺北市,' + line.strip() + '&'
		# print(url)
		json_str = requests.get(url).text
		if json_str == '{\"type\":\"FeatureCollection\",\"features\":[]}':
			print(' --- EMPTY --- ' + file)
		# print('json',json_str)
		with open(json_file_path, 'w') as out_file:
			out_file.write(json_str)