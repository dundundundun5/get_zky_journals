import urllib.parse
import pandas as pd
import os
from argparse import ArgumentParser
import requests
import urllib
from bs4 import BeautifulSoup
parser = ArgumentParser()
parser.add_argument('--year',default='2018')
args = parser.parse_args()
YEAR = args.year

SUBJECTS=['地学','地学天文','工程技术','管理科学','化学','环境科学与生态学','农林科学','社会科学','生物','数学','物理','医学','综合性期刊']


PATH=f"./old_json_{YEAR}"



headers={
    "User-Agent":"Mozilla/5.0(Linux;Android6.0;Nexus5Build/MRA58N)AppleWebKit/537.36(KHTML,likeGecko)Chrome/131.0.0.0MobileSafari/537.36Edg/131.0.0.0",
    "Connection":"keep-alive",
    "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
    "Cookie":"Hm_lvt_0dae59e1f85da1153b28fb5a2671647f=1732063684,1732068719,1732078752,1732092279; HMACCOUNT=67BA1261474FAE44; ASP.NET_SessionId=dl5n1ycujp14ba0uycip1lur; __AntiXsrfToken=44374520e63d4cd8a1c41ec2d320673c; Hm_lpvt_0dae59e1f85da1153b28fb5a2671647f=1732092303",
    "Host":"www.fenqubiao.com",
    "Referer":"https://www.fenqubiao.com/Core/CategoryList.aspx",
}
def get_rid_of(a:str):
    
    a = a.replace('\n', "")
    a = a.replace('\r', "")
    a = a.replace(' ', "")
    return  a
def get_rid_of_alpha(b:str):

    import re
    b = b.lower()    
    b = re.sub('[a-z]', '',  b)
    
    b = b.replace('&', '')
    b = b.replace(' ', '')
    return b
data = {"y": "",
        "t": ""}
results = []
columns = columns=["刊名","中科院ID","年份","分区","ISSN","综述","开放","最低档","学科信息","学科"]
for subject in SUBJECTS:
    
    temp = pd.read_csv(f"{PATH}/{subject}.csv")
    for i in range(len(temp)):
        name = temp.name[i]
        data['y'] = YEAR
        data['t'] = urllib.parse.quote(name)
        url=f"https://www.fenqubiao.com/Core/JournalDetail.aspx?y={data['y']}&t={data['t']}"
        response =requests.post(url=url, headers=headers, data=data)
        # 解析网页并获取内容变成数组
        response_soup =  BeautifulSoup(response.text, 'lxml')
        with open('a.html', mode='w', encoding='utf-8') as f:
            f.write(response.text)
        trs = response_soup.find("body").find('form').find_all('div')[6].find('div').find('table').find('tbody').find_all('tr')
        
        journal_name = trs[0].find_all('td')[1].text
        issn = trs[1].find_all('td')[3].text
        is_review =  trs[2].find_all('td')[3].text
        all_info = trs[3].find('td').find('table').find('tbody').find_all('tr')
        subject_info = {}
        info_temp = ''
        section = 0
        lowest = -1
        for i, info in enumerate(all_info):
            if i== 0:
                continue
            a = info.find_all('td')
            b = get_rid_of(a[2].text)
            c = get_rid_of_alpha(a[1].text)
            if lowest <= int(b):
                lowest = int(b)
            if a[0].text == '小类':
                
                subject_info[a[1].text] = b
                info_temp += ','
                info_temp += c
            if a[0].text == '大类':
                subject_info[a[1].text] = b
                info_temp = c + info_temp
                section = b
        result = [journal_name, '0', YEAR, section, issn, is_review, '未收录', lowest, subject_info, info_temp]
        print(result)
        results.append(result)


results =  pd.DataFrame(results, columns=columns)
results.to_excel(f"中科院{YEAR}旧版.xlsx", index=False)

