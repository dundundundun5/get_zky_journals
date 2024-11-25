# "每天勤换Cookie"
import urllib.parse
import requests
from bs4 import BeautifulSoup
import urllib
import math
from argparse import ArgumentParser
from .zky_properties import COOKIE,USER_AGENT
parser = ArgumentParser()
parser.add_argument('--year', default='2019', choices=['2018', '2019', '2020', '2021'])
parser.add_argument('--subject', default='地学', required=True)
args = parser.parse_args()
YEAR = args.year
SUBJECT = args.subject

PATH =f"./old_json_{YEAR}"

manager = ['ctl00$ContentPlaceHolder1$ajaxManager|ctl00$ContentPlaceHolder1$dplYear','ctl00$ContentPlaceHolder1$ajaxManager|ctl00$ContentPlaceHolder1$dplCategory','ctl00$ContentPlaceHolder1$udpSelectItem|ctl00$ContentPlaceHolder1$btnSearch',
'ctl00$ContentPlaceHolder1$ajaxManager|ctl00$ContentPlaceHolder1$AspNetPager1']
data = {
    "ctl00$ContentPlaceHolder1$ajaxManager": "",
    "ctl00$ContentPlaceHolder1$dplCategoryType":"0",
    "ctl00$ContentPlaceHolder1$dplSection":"0",
    "ctl00$ContentPlaceHolder1$dplYear":"",
    "ctl00$ContentPlaceHolder1$dplCategory":"",
    "ctl00$ContentPlaceHolder1$dplSort":"0",
    "__EVENTTARGET": "",
    "__EVENTARGUMENT": "",
    "_TSM_HiddenField_": "",
    "__VIEWSTATE":"",
    "__VIEWSTATEGENERATOR": "",
    "__EVENTVALIDATION": "",
    "__ASYNCPOST": "true",
}
url = "https://www.fenqubiao.com/Core/CategoryList.aspx"
headers = {
    "User-Agent": USER_AGENT,
    "Connection":"keep-alive",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": COOKIE,
    "Host":"www.fenqubiao.com",
    "Origin":"https://www.fenqubiao.com",
    "Referer":"https://www.fenqubiao.com/Core/CategoryList.aspx",
    }
def get_token(text):
    soup = BeautifulSoup(text, "lxml")
    viewstate = soup.find_all(attrs={'class':'aspNetHidden'})[0].find(attrs={'name':'__VIEWSTATE'})['value']
    eventvalidation = soup.find_all(attrs={'class':'aspNetHidden'})[1].find(attrs={'name':'__EVENTVALIDATION'})['value']
    viewstate_gen = soup.find_all(attrs={'class':'aspNetHidden'})[1].find(attrs={'name':'__VIEWSTATEGENERATOR'})['value']
    tsm = soup.find_all(attrs={'class':'aspNetHidden'})[0].find(attrs={'name':'_TSM_HiddenField_'})['value']
    return tsm, viewstate, eventvalidation, viewstate_gen
def renew_token(index):
    tokens = index.text.split("\n")[-1]
    tokens = tokens.replace(" ", "").split("|")
    for i,a in enumerate(tokens):
        if a == '__VIEWSTATE':
            data["__VIEWSTATE"] = tokens[i + 1]
        if a == '__EVENTVALIDATION':
            data['__EVENTVALIDATION']  = tokens[i + 1]  
index = requests.post(url=url,headers=headers)

# token填写
data["_TSM_HiddenField_"], data["__VIEWSTATE"],data['__EVENTVALIDATION'],data['__VIEWSTATEGENERATOR'] = get_token(index.text)

# manager改变,申请
data['ctl00$ContentPlaceHolder1$ajaxManager'] = manager[0]
data['__EVENTTARGET'] = manager[0].split('|')[-1]
data['ctl00$ContentPlaceHolder1$dplYear'] = YEAR
year_index = requests.post(url=url, headers=headers, data=data)

# token 更新
renew_token(year_index)
# manager改变
data['ctl00$ContentPlaceHolder1$ajaxManager'] = "ctl00$ContentPlaceHolder1$ajaxManager|ctl00$ContentPlaceHolder1$dplCategory"
data['__EVENTTARGET'] = "ctl00$ContentPlaceHolder1$dplCategory"
data['ctl00$ContentPlaceHolder1$dplCategory'] = SUBJECT
category_index = requests.post(url=url, headers=headers, data=data)

# token 更新
renew_token(category_index)
data['ctl00$ContentPlaceHolder1$ajaxManager'] = "ctl00$ContentPlaceHolder1$ajaxManager|ctl00$ContentPlaceHolder1$AspNetPager1" 
data['__EVENTTARGET'] = "ctl00$ContentPlaceHolder1$AspNetPager1"
data['__EVENTARGUMENT'] = '1'

# 第一页获取
any_page = requests.post(url=url, headers=headers, data=data)

# 计算一共多少页
any_page_soup = BeautifulSoup(any_page.text, 'lxml')
max_journals = any_page_soup.find("div").find("div").find_all("span")[1].text
max_journals = int(max_journals)
max_pages  = int(math.ceil(max_journals / 20)) 

import pandas as pd
res  = []

# 第二页开始循环获取
for i in range(2, max_pages + 1):
    #
    # 处理第一页的期刊信息记录title
    any_page_soup = BeautifulSoup(any_page.text, 'lxml')
    tbody = any_page_soup.find("div").find("div").find("table").find("tbody")
    trs = tbody.find_all("tr")
    for tr in trs:
        name = tr.find_all("td")[1].find("a").text
        res.append(name)
        print(name)
    renew_token(any_page)
    data['__EVENTARGUMENT'] = f'{i+1}'
    any_page = requests.post(url=url, headers=headers, data=data)

res = pd.DataFrame(res, columns=['name'])
import os
os.makedirs(PATH, exist_ok=True)

res.to_csv(f"{PATH}/{SUBJECT}.csv",index=False)
print("=================================================")
