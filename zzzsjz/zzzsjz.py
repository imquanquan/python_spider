#! /usr/bin/env python3.6

import requests
from collections import namedtuple
import pandas as pd
from pyquery import PyQuery as pq

SEED_URL = "http://www.zzzs.wang/a/gaoxiaozizhuzhaoshengjianzhang/zzzs/2018/0305/5620.html"
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

def crawl_jz(jz_url, name):
    jz_doc = pq(requests.get(jz_url).content.decode('gbk'))
    body = pq(jz_doc('.m4_box6').children()[:-6])
    html = HTML_HEAD + str(body) + HTML_TAIL
    with open(name + '.html', 'w') as f:
        f.write(html)
        
school_df = pd.DataFrame(columns=['name', 'jz_url', 'sign_up_time', 'ass_time', 'ass_type'])

seed_doc = pq(requests.get(SEED_URL).content.decode('gbk'))

num = 0
for tr in list(seed_doc("tbody tr").items())[2:]:
    td_list = list(tr('td').items())
    flag = 0
    if len(td_list) == 7:
        flag = 1
    name = td_list[flag].text()
    jz_url = td_list[flag+1]('a').attr.href
    sign_up_time = td_list[flag+2].text()
    ass_time = td_list[flag+3].text()
    ass_type = td_list[flag+4].text()
    school_df.loc[num] = [name, jz_url, sign_up_time, ass_time, ass_type]
    num += 1
    print(jz_url)
    try:
        crawl_jz(jz_url, name)
    except:
        print('e')

