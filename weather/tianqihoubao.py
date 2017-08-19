#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-08-15 23:38:41
# Project: tianqihoubao


import re
import csv
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }
    
    def __init__(self):
        self.base_url = "http://www.tianqihoubao.com/lishi/guangzhou/month/"
        self.start_year = 2011
        self.csv_head = ('日期','天气状况','气温','风力风向')

    @every(minutes=24 * 60)
    def on_start(self):
        for year in range(self.start_year,2018):
            for month in range(1,13):
                self.crawl("%s%d%02d.html"%(self.base_url,year,month),
                           callback=self.index_page,
                           save={'year': year,'month': month})

        
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('table').items():
            html = re.sub(r'\s+','',str(each).replace('&#13;',''))
            data_re = re.compile(r'报">(.*?)</a></td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>')
            datas = re.findall(data_re,html)
            with open("/home/imquanquan/weather/tianqihoubao/%d%02d.csv"%(response.save['year'],response.save['month']),"w") as f:
                writer = csv.writer(f)
                writer.writerow(self.csv_head)
                for data in datas:
                    writer.writerow(data)
