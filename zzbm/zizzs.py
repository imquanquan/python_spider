#!/usr/bin/env python3

import requests
from pyquery import PyQuery as pq
import re


BASE_URL = "http://www.zizzs.com"
SEED_URL = "http://www.zizzs.com/c/201803/22129.html"
HTML_HEAD = '''
<html xmlns="http://www.w3.org/1999/xhtml"><head>
<meta http-equiv="Content-Type" content="text/html; charset=utf8">
</head>
<body>
'''
HTML_TAIL = '''
</body>
</html>
'''
area_re = re.compile(r'针对(.*)招生')

def crawl_jz(jz_url, name):
    jz_doc = pq(requests.get(url).content.decode('utf8'))
    body = pq(jz_doc('#content').children()[:-4])
    html = HTML_HEAD + str(body) + HTML_TAIL
    with open(name + '.html', 'w') as f:
        f.write(html)

doc = pq(requests.get(SEED_URL).content.decode('utf8')
        
for tr in doc('tr').items():
    if area_re.findall(tr.text()):
        area = area_re.findall(tr.text())[0]
    if tr('td a'):
        name = list(tr('td').items())[0].text()
        url = BASE_URL + tr('tr a').attr.href
        crawl_jz(url, area + '_' + name))
