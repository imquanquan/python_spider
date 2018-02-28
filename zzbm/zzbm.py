#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import re
import requests
from pyquery import PyQuery as pq

CODE = '''<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>
'''
DEL_RE = re.compile(r'''声明.*?由自主招生在线团队（微信公众号：zizzsw）排版编辑，如有侵权，请及时联系管理员删除。''')
DOWNLOAD_RE = re.compile(r'''<a class="download".*?</a>''')

def crawl_detail_page(url):
    detail_doc = pq(requests.get(url).content.decode('utf8'))
    name = detail_doc('h1').text() + '.html'
    div = detail_doc('#content')[0]
    detail = str(pq(div[:-1]))
    detail = re.sub(DEL_RE, '', detail)
    detail = re.sub(DOWNLOAD_RE, '', detail)
    if name:
        return name, CODE + detail
    return None, None

def save_file(name, html):
    with open(name, 'w') as f:
        f.write(html)


response = requests.get('http://www.zizzs.com/zt/zzzsjz2017/')
html = response.content.decode('utf8')
doc = pq(html)
for each in doc('.ds2017 a').items():
    if each.attr.href.strip() != '###':
        name, html = crawl_detail_page(each.attr.href.strip())
        print(name)
        if name:
            save_file(name, html)
