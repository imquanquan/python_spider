#!/usr/bin/env python3.6

import re
import requests
from pyquery import PyQuery as pq


BASE_URL = 'http://gaokao.chsi.com.cn'
SEED_URL = 'http://gaokao.chsi.com.cn/gkzt/gspyst2018'
LINK_URL_RE = re.compile(r'''<td>(.*?)</td>\r\n\t<td><a href="(.*?)" target="_blank">点击查看</a>''')
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

def detail_crawl(url, name):
    doc = pq(requests.get(url).text)
    mess = doc('.content-l').html()
    if mess:
        with open(name, 'w') as f:
            #f.write(HTML_HEAD + mess + HTML_TAIL)
            f.write(HTML_HEAD + mess + HTML_TAIL)
    else:
        print(name)
        

if __name__ == '__main__':
    html = requests.get(SEED_URL).text
    for name, link in LINK_URL_RE.findall(html):
        print(BASE_URL+link)
        detail_crawl(BASE_URL+link, name+'2018年高水平艺术团招生简章.html')    