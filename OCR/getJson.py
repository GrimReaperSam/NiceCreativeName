# coding=UTF-8

import os
import requests

for root, dirs, files in os.walk('LandNumber/'):
    for file in files:
        if file.endswith(".csv"):

            url = 'http://twland.ronny.tw/index/search?'

            csv_file = open('LandNumber/' + file, 'r')
            print("[Dealing] " + file)
            for line in csv_file.readlines():
                url += 'lands[]=臺北市,' + line.strip() + '&'
            # print(url)
            json_str = requests.get(url).text
            if json_str == '{\"type\":\"FeatureCollection\",\"features\":[]}':
                print(' --- EMPTY --- ' + file)
            # print('json',json_str)
            json_file = os.path.splitext(file)[0] + '.json'
            with open('GeoJson/' + json_file, 'w') as out_file:
                out_file.write(json_str)