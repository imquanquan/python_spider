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
            'Referer' : 'http://www.tqyb.com.cn/gz/weatherLive/radar/',
            'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
a_day_ago = (datetime.now() - timedelta(2/3)).strftime("%Y-%m-%d %H:%M:%S")
date_list = datelist(a_day_ago, now, "6min")

# 程序每天定时在晚上8点运行。爬昨天晚8点到今天晚8点的数据，雷达图间隔6分钟一张。

error = requests.get("http://www.tqyb.com.cn/data/radar/gz/19/20171019/Z9200_201710190000Z_PPI_02_19.png", headers=headers).content

# 错误页面实例

for date in date_list:
    year = datetime.strftime(date, "%y")
    month = datetime.strftime(date, "%m")
    day = datetime.strftime(date, "%d")
    hour = datetime.strftime(date, "%H")
    minute = datetime.strftime(date, "%M")

    link = "http://www.tqyb.com.cn/data/radar/gz/19/2017" + month + day + "/Z9200_2017" + month + day + str(int(hour) - 8).zfill(2) + minute + "Z_PPI_02_19.png"
    image = requests.get(link, headers=headers).content
    print(link)

    if image != error:
        with open("gd/" + year + month + day + hour + minute + "00.PNG", 'ab') as f:
            f.write(image)
    time.sleep(0.5)
