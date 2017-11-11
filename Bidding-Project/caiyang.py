#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

import re
import requests
from pyquery import PyQuery as pq
from Project import *

getfile_time_re = re.compile(r"(获取招标文件时间：.*?)\d、")
postfile_time_re = re.compile(r"(递交投标文件时间：.*?)\d、")
publicity_time_re = re.compile(r"公示时间：.*?[。）]")
review_time_re = re.compile(r"评审日期.*?日")
target_time_re = re.compile(r"定标日期.*?日")

base_url = "http://879085.254117.30la.com.cn/"

url_list = []
for i in range(1, 43):
    url = base_url + "info.php?catid=47&page=" + str(i)
    doc = pq(requests.get(url).text)
    for li in doc('ul li span a').items():
        for keyword in keywords:
            if keyword in li.text():
                pro_name = li.text()
                pro_url = base_url + li.attr.href
                url_list.append(pro_url)
           

for url in url_list:
    html = requests.get(url).text
    doc = pq(html)
    clear_doc = re.sub(r'\s', '', doc.text())
    print(url)
    print(getfile_time_re.findall(clear_doc))
    print(postfile_time_re.findall(clear_doc))
    print(publicity_time_re.findall(clear_doc))
    

for i in range(1, 39):
    url = base_url + "info.php?catid=49&page=" + str(i)
    doc = pq(requests.get(url).text)
    for li in doc('ul li span a').items():
        for keyword in keywords:
            if keyword in li.text():
                pro_name = li.text()
                pro_url = base_url + li.attr.href
                url_list.append(pro_url)
            
for url in url_list:
    html = requests.get(url).text
    doc = pq(html)
    clear_doc = re.sub(r'\s', '', doc.text())
    print(url)
    print(review_time_re.findall(clear_doc))
    print(target_time_re.findall(clear_doc))

