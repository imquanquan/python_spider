#!/usr/bin/env python3.6

import re
import time

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd

# 匹配最大页数
PAGE_NUM_RE = re.compile(r"ANPager','(\d+)'\)\" style=\"margin-right:8px;\"><img src=\"/images/PageNavi/lastn.gif\"")
# 匹配报告 id
ID_RE = re.compile(r'ShowPort\((\d+),2016\)')

# 爬每个页面信息的函数
def crawl(city, county):
    global num
    items = browser.find_elements_by_xpath("//tr[@style='line-height: 23px;']")
    for item in items:
        informations = item.text.split(' ')
        informations[3] = ID_RE.findall(item.find_element_by_link_text('2016年度报告').get_attribute('onclick'))[0]
        pros_df.loc[num] = [informations[1], informations[2], informations[3], city, county]
        num += 1
        
browser = webdriver.Firefox()
browser.get('http://gdchzz.nasg.gov.cn/Index/QueryList.aspx#fragment-2')
# 隐式等待时间
browser.implicitly_wait(3)

# 三个选项框
select_province = Select(browser.find_element_by_name('sltProvince'))
select_city = Select(browser.find_element_by_name('sltCity'))
select_county = Select(browser.find_element_by_name('sltCounty'))

# 年度按钮
search = browser.find_element_by_id('Annual')
search.click()

pros_df = pd.DataFrame(columns=['所在地区', '单位名称', 'id', '市', '区'])
num = 0

# 搜索按钮
annual_report = browser.find_element_by_id('BtnAnnual')

for province_index in range(1, len(select_province.options)):
    select_province.select_by_index(province_index)

    for city_index in range(1, len(select_city.options)):
        select_city.select_by_index(city_index)
        city = select_city.first_selected_option.text

        if len(select_county.options) != 1:
            
            for county_index in range(1, len(select_county.options)):
                select_county.select_by_index(county_index)
                county = select_county.first_selected_option.text
                annual_report.click()
                
                if PAGE_NUM_RE.findall(browser.page_source):
		    # 多于一页的情况                
                    time.sleep(1)
                    for page in range(1, int(PAGE_NUM_RE.findall(browser.page_source)[0])+1):
                        browser.execute_script("__doPostBack('PageTurnControl2$ANPager','%d')" % page)
                        time.sleep(1)
                        crawl(city, county)
                    time.sleep(1)

                    browser.execute_script("__doPostBack('PageTurnControl2$ANPager','1')")
                else:
		    # 只有一页的情况
                    crawl(city, county)
        else:
	    # 没选项的特殊情况=。=
            county = ''
            annual_report.click()
            if PAGE_NUM_RE.findall(browser.page_source):
                time.sleep(1)
                for page in range(1, int(PAGE_NUM_RE.findall(browser.page_source)[0])+1):
                    browser.execute_script("__doPostBack('PageTurnControl2$ANPager','%d')" % page)
                    time.sleep(1)
                    crawl(city, county)
                browser.execute_script("__doPostBack('PageTurnControl2$ANPager','1')")
            else:
                crawl(city, county)

print(pros_df)
