#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-08-05 23:58:54
# Project: gdwater

import os
import re
import pdfkit
import requests
from pyspider.libs.base_handler import *


DIR_PATH = '/home/imquanquan/a/'

class Handler(BaseHandler):
    crawl_config = {
    }
    def __init__(self):
        self.deal = Deal()

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://bg.imquanquan.net/list.html', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        base_link = 'http://www.gdwater.gov.cn/xxgk/006939748'
        categories_re = re.compile(r'<div class=" Page"><a href="(.*?)".*?id=".*?">(.*?)</a>\((.*?)\)</div>')
        categories = re.findall(categories_re,str(next(response.doc('div').items())))
        for each in categories[:23]:
            dir_path = self.deal.mkDir(each[1].replace(' ', ''))+'/'
            print(dir_path)
            page_count = int(each[2]) // 20 + 1
            self.crawl(base_link+each[0][24:], callback=self.detail_page,save={'dir_path': dir_path})
            for i in range(1,page_count):
                self.crawl(base_link+each[0][24:]+'list_'+str(i)+'.htm', callback=self.detail_page,
                          save={'dir_path': dir_path})

    @config(priority=2)
    def detail_page(self, response):
         for each in response.doc('.mc div a').items():
             self.crawl(each.attr.href, callback=self.download_page,
                        save={'dir_path': response.save['dir_path']})
         
    def download_page(self, response):
        file_name = response.save['dir_path'] + response.doc('title').text().replace(' ', '') + '.pdf'
        pdfkit.from_url(response.url,file_name)
        for each in response.doc('ul > a').items():
             r = requests.get(each.attr.href)
             with open("/home/imquanquan/a/%s"%(each.text()), "wb") as f:
                 f.write(r.content)
                    
class Deal(object):
    def __init__(self):
        self.path = DIR_PATH
 
    def mkDir(self, path):
        path = path.strip()
        dir_path = self.path + path
        exists = os.path.exists(dir_path)
        if not exists:
            os.makedirs(dir_path)
            return dir_path
        else:
            return dir_path
