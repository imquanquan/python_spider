#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from datetime import datetime,timedelta
import requests
import pandas as pd
import time

def datelist(beginDate, endDate, freq):
    date_l = [x for x in list(pd.date_range(start = beginDate, end = endDate, freq = freq))]
    return date_l

headers = {
            'Referer' : 'http://products.weather.com.cn/product/radar/index/procode/JC_RADAR_AZ9200_JB.shtml',
            'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
half_a_day_ago = (datetime.now() - timedelta(0.5)).strftime("%Y-%m-%d %H:%M:%S")
date_list = datelist(half_a_day_ago, now, "6min")

# 程序每天定时在晚上8点运行。爬每天早8点到晚8点的数据，雷达图间隔6分钟一张。

error = requests.get("http://i.weather.com.cn/i/product/pic/l/sevp_aoc_rdcp_sldas_ebref_az9200_l88_pi_20171020010000000.png", headers=headers).content

# 错误页面实例

for date in date_list:
    year = datetime.strftime(date, "%y")
    month = datetime.strftime(date, "%m")
    day = datetime.strftime(date, "%d")
    hour = datetime.strftime(date, "%H")
    minute = datetime.strftime(date, "%M")

    link = "http://i.weather.com.cn/i/product/pic/l/sevp_aoc_rdcp_sldas_ebref_az9200_l88_pi_2017" \
            + month + day + str(int(hour) - 8).zfill(2) + minute + "00000.png"
    print(link)
    
    image = requests.get(link, headers=headers).content
    if image != error:
        with open("china/" + year + month + day + hour + minute + "00.PNG", 'ab') as f:
            f.write(image)

    time.sleep(0.5)
