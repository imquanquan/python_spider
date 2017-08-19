#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-08-04 22:28:06
# Project: env_impact

import re
import pdfkit
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://bg.imquanquan.net/shit.html', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl('http://58.248.45.69:30001'+each.attr.href[24:], callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        s = str(next(response.doc('html').items()))
        name_re = re.compile(r'<td colspan="3">(.*?)</td>')
        name = re.findall(name_re,s)[0]
        pdfkit.from_url(response.url,'/home/imquanquan/gdep/%s.pdf'%(name))
