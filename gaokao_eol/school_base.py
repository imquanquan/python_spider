#!/usr/bin/env python3.6
#! -*- coding:utf-8 -*-

import json
import requests
from urllib.parse import urlencode

import pandas as pd


BASE_URL = 'https://data-gkcx.eol.cn/soudaxue/queryschool.html?'
data = {
    'messtype':'jsonp',
    # 'callback':'jQuery18306276143066198141_1515982696687',
    'province':'',
    'schooltype':'',
    'page': '',
    'size':'30',
    'keyWord1':'',
    'schoolprop':'',
    'schoolflag':'',
    'schoolsort':'',
    'schoolid':'',
    # '_':'1515982697498'
}
headers = {
            'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36' ,
            'Referer' : 'http://gkcx.eol.cn/soudaxue/queryschool.html?messtype=jsonp',
            'Host' : 'data-gkcx.eol.cn'    
        }

count = 0
for page in range(1, 94):
    data['page'] = str(page)
    url = BASE_URL + urlencode(data, encoding = 'utf8')
    school_data = requests.get(url, headers = headers).text
    json_data = json.loads(school_data[5:-2])
    if page == 1:
        school_df = pd.DataFrame(columns=json_data['school'][0].keys())
    for item in range(0, len(json_data['school'])):
        for key in json_data['school'][item].keys():
            school_df.loc[count,key] = json_data['school'][item][key]
        count += 1
        
writer = pd.ExcelWriter('中国教育在线.xls')
school_df.to_excel(writer, '中国教育在线')
writer.save()