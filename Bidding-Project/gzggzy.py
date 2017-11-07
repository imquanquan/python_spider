#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

import requests
import pandas as pd
from Project import *
from bs4 import BeautifulSoup


if __name__ == "__main__":
    headers = {
                'Referer' : 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=505',
                'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }
    base_url = 'http://www.gzggzy.cn/cms/wz/view/scxx/zbxx_new.jsp?'

    for keyword in keywords:
        data = {
            'page' : '1',
            'xmbh' : '',
            'xmmc' : keyword,
            'fbrq' : ''
        }
        html = post_and_get_html(base_url, data, 'gbk')
        soup = BeautifulSoup(html, 'html.parser')
        projects = soup.find_all('tr')[1::4]
        for project in projects:
            pro_name = project.find_all('td')[2].text.strip()
            pro_area = '广州'
            pro_amount = project.find_all('td')[6].text.strip() + '：' + project.find_all('td')[7].text.strip()
            pro_date = project.find_all('td')[-1].text.strip()
            pro = Project(pro_name, pro_date, pro_amount, pro_area)
            pro.insert()

    writer = pd.ExcelWriter('project.xlsx')
    Project.pros_df.to_excel(writer,'gzggzy')
    writer.save()

