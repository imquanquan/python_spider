#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-08-02 17:58:08
# Project: water_conservancy

import os
from pyspider.libs.base_handler import *

DIR_PATH = '/home/imquanquan/water_conservancy/'

class Handler(BaseHandler):
    crawl_config = {
    }
    def __init__(self):
        self.deal = Deal()
     
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.gdwater.gov.cn/xxgk/sltjsbzzt/stbc/index.html', callback=self.index_page)
    
           
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for url in response.doc('#treeContainer > ul > div > a[href^="http"]').items():
            self.crawl(url.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        for each in response.doc('td > a[href^="http"]').items():
            name = each.text()
            dir_path = self.deal.mkDir(name.replace(' ', ''))+'/'
            print(dir_path)
            self.crawl(each.attr.href, callback=self.file_page,
                      save={'dir_path': dir_path})
        
    def file_page(self,response):
        for each in response.doc('li > a[href^="http"]').items():
            file_name = response.save['dir_path']+each.text()
            print(file_name)
            self.crawl(each.attr.href, callback=self.download_file,
                       save={'file_name': file_name})
        
    def download_file(self, response):
        content = response.content
        with open(response.save['file_name'],'wb') as f:
            f.write(content)
        

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
