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
arr_subject_en =   [
                        [ "哲学" ],
                        [ "理论经济学", "应用经济学" ],
                        [ "法学", "政治学", "社会学", "民族学", "马克思主义理论" ],
                        [ "教育学", "心理学", "体育学" ],
                        [ "中国语言文学", "外国语言文学", "新闻传播学" ],
                        [ "考古学", "中国史", "世界史" ],
                        [ "数学", "物理学", "化学", "天文学", "地理学", "大气科学", "海洋科学", "地球物理学", "地质学",
                          "生物学", "生态学", "统计学" ],
                        [ "力学", "机械工程", "光学工程", "仪器科学与技术", "材料科学与工程", "冶金工程", "动力工程及工程热物理",
                          "电气工程", "电子科学与技术", "信息与通信工程", "控制科学与工程", "计算机科学与技术", "建筑学",
                                        "土木工程", "水利工程", "测绘科学与技术", "化学工程与技术", "地质资源与地质工程", "矿业工程",
                                        "石油与天然气工程", "纺织科学与工程", "轻工技术与工程", "交通运输工程", "船舶与海洋工程",
                                        "航空宇航科学与技术", "核科学与技术", "农业工程", "环境科学与工程", "生物医学工程",
                                        "食品科学与工程", "城乡规划学", "软件工程", "安全科学与工程" ],
                        [ "作物学", "园艺学", "农业资源与环境", "植物保护", "畜牧学", "兽医学", "林学", "水产", "草学" ],
                        [ "基础医学", "临床医学", "口腔医学", "公共卫生与预防医学", "中医学", "中西医结合", "药学", "中药学",
                          "特种医学", "护理学" ],
                        [ "管理科学与工程", "工商管理", "农林经济管理", "公共管理", "图书情报与档案管理" ],
                        [ "艺术学理论", "音乐与舞蹈学", "戏剧与影视学", "美术学", "设计学" ], ]


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

arr_subject_list = sum(arr_subject_en, [])
arr_subject_link_list = sum(arr_subject_link, [])

i = 0
for arr_subject in arr_subject_link_list:
    url = base_url + arr_subject + '.html'
    html_source = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(html_source, 'html.parser')
    for rank_data in soup.find_all('tr', class_='bgfd'):
        subject = arr_subject_list[arr_subject_link_list.index(arr_subject)]
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
