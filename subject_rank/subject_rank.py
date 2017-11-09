#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

df = pd.DataFrame(columns=['subject', 'rank', 'percentile', 'university_name', 'PhD', 'core_subject', 'score'])
base_url = "http://www.zuihaodaxue.com/BCSR/"
RankData_re = re.compile(r'^(\d+)(前\d+%)(.*?)(\d+)$')
PhD_re = re.compile(r'.级学科博士学位授权点')
core_subject_re = re.compile(r'.级学科国家重点学科')

arr_subject_link = [
			[ "zhexue2017" ],
			[ "lilunjingjixue2017", "yingyongjingjixue2017" ],
			[ "faxue2017", "zhengzhixue2017", "shehuixue2017", "minzuxue2017", "makesizhuyililun2017" ],
			[ "jiaoyuxue2017", "xinlixue2017", "tiyuxue2017" ],
			[ "zhongguoyuyanwenxue2017", "waiguoyuyanwenxue2017", "xinwenchuanboxue2017" ],
			[ "kaoguxue2017", "zhongguoshi2017", "shijieshi2017" ],
			[ "shuxue2017", "wulixue2017", "huaxue2017", "tianwenxue2017", "dilixue2017", "daqikexue2017", "haiyangkexue2017", "diqiuwulixue2017", "dizhixue2017",
					"shengwuxue2017", "shengtaixue2017", "tongjixue2017" ],
			[ "lixue2017", "jixiegongcheng2017", "guangxuegongcheng2017", "yiqikexueyujishu2017", "cailiaokexueyugongcheng2017", "yejingongcheng2017", "dongligongchengjigongchengrewuli2017",
					"dianqigongcheng2017", "dianzikexueyujishu2017", "xinxiyutongxingongcheng2017", "kongzhikexueyugongcheng2017", "jisuanjikexueyujishu2017", "jianzhuxue2017",
					"tumugongcheng2017", "shuiligongcheng2017", "cehuikexueyujishu2017", "huaxuegongchengyujishu2017", "dizhiziyuanyudizhigongcheng2017", "kuangyegongcheng2017",
					"shiyouyutianranqigongcheng2017", "fangzhikexueyugongcheng2017", "qinggongjishuyugongcheng2017", "jiaotongyunshugongcheng2017", "chuanboyuhaiyanggongcheng2017",
					"hangkongyuhangkexueyujishu2017", "hekexueyujishu2017", "nongyegongcheng2017", "huanjingkexueyugongcheng2017", "shengwuyixuegongcheng2017",
					"shipinkexueyugongcheng2017", "chengxiangguihuaxue2017", "ruanjiangongcheng2017", "anquankexueyugongcheng2017" ],
			[ "zuowuxue2017", "yuanyixue2017", "nongyeziyuanyuhuanjing2017", "zhiwubaohu2017", "chumuxue2017", "shouyixue2017", "linxue2017", "shuichan2017", "caoxue2017" ],
			[ "jichuyixue2017", "linchuangyixue2017", "kouqiangyixue2017", "gonggongweishengyuyufangyixue2017", "zhongyixue2017", "zhongxiyijiehe2017", "yaoxue2017", "zhongyaoxue2017",
					"tezhongyixue2017", "hulixue2017" ],
			[ "guanlikexueyugongcheng2017", "gongshangguanli2017", "nonglinjingjiguanli2017", "gonggongguanli2017", "tushuqingbaoyudanganguanli2017" ],
			[ "yishuxuelilun2017", "yinyueyuwudaoxue2017", "xijuyuyingshixue2017", "meishuxue2017", "shejixue2017" ], ]

i = 0
for arr_subject in sum(arr_subject_link, []):
    url = base_url + arr_subject + '.html'
    html_source = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(html_source, 'html.parser')
    for rank_data in soup.find_all('tr', class_='bgfd'):
        subject = arr_subject[:-4]
        rank, percentile, university_name, score = RankData_re.findall(rank_data.text)[0]
        if PhD_re.findall(str(rank_data)):
            PhD = PhD_re.findall(str(rank_data))[0]
        else:
            PhD = ''
        if core_subject_re.findall(str(rank_data)):
            core_subject = core_subject_re.findall(str(rank_data))[0]
        else:
            core_subject = ''
        df.loc[i] = [subject, rank, percentile, university_name, PhD, core_subject, score]
        i += 1

writer = pd.ExcelWriter('学科排名.xlsx')
df.to_excel(writer,'学科排名')
writer.save()
