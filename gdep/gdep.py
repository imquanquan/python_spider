#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-08-03 07:23:24
# Project: gdep

import re
import os
import pdfkit
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
        'fetch_type' : 'js',
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.gdep.gov.cn/zcfg/dfguizhang/?sTop=200', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.list-leader a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        page_re = re.compile(r"总共(.*?)页")
        page = re.findall(page_re,str(response.doc('font')))
        self.crawl(response.url, callback=self.list_page)
        if page:
            for i in range(1,int(page[0])):
                self.crawl(response.url+'index_'+str(i)+'.html', callback=self.list_page)
    
    def list_page(self, response):
        for each in response.doc('.titlelie[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.download_page,save={'title': each.text()})
        
    def download_page(self, response):
        try:
            pdfkit.from_url(response.url,'/home/imquanquan/gdep/%s.pdf'%(response.save['title']))
        except:
            pass