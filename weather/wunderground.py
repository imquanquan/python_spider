#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-08-16 01:31:10
# Project: wunderground

import csv
import pandas as pd
from datetime import datetime
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        for date in datelist('20010101','20170816'):
            year = date[0:4]
            month = date[5:7]
            day = date[8:10]
            self.crawl('https://www.wunderground.com/history/airport/ZGGG/'+year+'/'+month+'/'+day+'/DailyHistory.html?eq_city=广州&req_state=44&req_statename=China', 
                       callback=self.index_page,
                       save={'year' : year,
                             'month' : month,
                             'day' : day})

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        with open('/home/imquanquan/weather/wunderground/'+response.save['year']+response.save['month']+response.save['day']+'.csv',
                      'w') as f:
            f.write('时间,温度,风冷温,露点,湿度,气压,能见度,风向,风速,瞬时风速,Precip,活动,状况\n')
            writer = csv.writer(f)
            for each in response.doc('.no-metars').items():
                data = []
                for item in each('td').items():
                    data.append(item.text())
                writer.writerow(data)
        
def datelist(beginDate, endDate):
    date_l=[datetime.strftime(x,'%Y-%m-%d') for x in list(pd.date_range(start=beginDate, end=endDate))]
    return date_l
''''''
