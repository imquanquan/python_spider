#/usr/bin/env python3
#-*- coding:utf-8 -*-

import re
import time
import json
from selenium import webdriver
from pyquery import PyQuery as pq


def crawl_data():
    #获取当前时间
    date_time = time.strftime("%Y-%m-%d%H", time.localtime()) 
    doc = pq(browser.page_source)
    try:
        TOC = doc('#TOC').text()
        levelTOC = doc('#levelTOC').text() 
    except:
        TOC = None
        levelTOC = None     
    data = {    
        'date' : doc('#date').text(),
        'time' : doc('#time').text(),
        'title' : doc('#title').text(),
        'NH3N' : doc('#NH3N').text(),
        'DO' : doc('#DO').text(),
        'pH' : doc('#pH').text(),
        'COD' : doc('#COD').text(),
        'propertysta' : doc('#propertysta').text(),
        'statussta' : doc('#statussta').text(),
        'TOC' : TOC,
        'levelpH' : doc('#levelpH').text(),
        'levelDO' : doc('#levelDO').text(),
        'levelNH3N' : doc('#levelNH3N').text(),
        'levelTOC' : levelTOC,
        'levelCOD' : doc('#levelCOD').text()
    }
    print(data)
    #将字典写入json文件
    jsObj = json.dumps(data,ensure_ascii=False)+'\n'
    with open('%s'%(date_time), 'a') as f:
        f.write(jsObj)  
    
showinfos_re = re.compile(r'"(showinfos\(.*?)"')
browser = webdriver.PhantomJS()
browser.get('http://58.68.130.147/')
#获取按下河流圆点时运行的js代码
js_code = re.findall(showinfos_re,browser.page_source)
for js in js_code:
    browser.execute_script(js)
    crawl_data()    

