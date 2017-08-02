#/usr/bin/env python3 
#-*- coding:utf-8 -*-

import re
import os
import time
import json
import pdfkit
from selenium import webdriver
from pyquery import PyQuery as pq

os.chdir("/home/imquanquan/gdwater")
browser = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
browser.get('http://www.gdwater.gov.cn/govsearch/simp_gov_list.jsp')
for i in range(1,1253):
    print(i)
    #执行翻页的js代码
    browser.execute_script('PageContext.PageNav.go(%d,1256);'%(i))
    time.sleep(2)
    doc = pq(browser.page_source)
    for each in doc('.mc a[href^="http"]').items():
        url = each.attr.href
        title = each.text().replace(' ', '')
        pdfkit.from_url(url,'%s.pdf'%(title))
        print(title)
        
