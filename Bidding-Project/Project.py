#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

import requests
import pandas as pd
from urllib.parse import urlencode

keywords = ['勘探', '勘测', '地理', '测绘', '测量']

class Project():
    pros_num = 0
    pros_df = pd.DataFrame(columns=['项目名称', '项目日期', '项目金额', '项目地区'])
    pros_name_list = []

    def __init__(self, pro_name, pro_date, pro_amount, pro_area):
        self.pro_name = pro_name
        self.pro_date = pro_date
        self.pro_amount = pro_amount
        self.pro_area = pro_area

    def __str__(self):
        return '项目名称：%s\n项目地区：%s\n项目金额：%s\n项目日期：%s' % \
        (self.pro_name, self.pro_area, self.pro_amount, self.pro_date)

    def insert(self):
        if self.pro_name not in Project.pros_name_list:
            Project.pros_name_list.append(self.pro_name)
            Project.pros_df.loc[Project.pros_num] = [self.pro_name, self.pro_date, self.pro_amount, self.pro_area]
            Project.pros_num = Project.pros_num + 1
            
def post_and_get_html(base_url, data, code):
    url = base_url + urlencode(data, encoding = code)
    return requests.get(url).text
