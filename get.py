# "每天勤换Cookie"
import requests
from argparse import ArgumentParser
from zky_properties import *
from json import loads, dumps
import pandas as pd
import requests
import re
import os
from bs4 import BeautifulSoup
from urllib.parse import quote
import warnings
warnings.filterwarnings("ignore")
parser = ArgumentParser()
parser.add_argument('--year', default='2025', choices=['2019', '2020', '2021', '2022', '2023', '2025'])
args = parser.parse_args()
year = args.year
subjects = eval(f"SUBJECTS_{year}")
path =f"./json_{year}"
final_path = f"./excel_{year}/"
SUBJECT = ""
json_exist = True

headers = {
    "User-Agent": USER_AGENT,
    "Connection":"keep-alive",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": COOKIE,
    "Host":"advanced.fenqubiao.com",
    }


def read_json(path, subject):
    f = open(f'{path}/{subject}.json', 'r')
    content = f.read()
    a = loads(content)
    result_json = []
    for i in range(len(a)):
        result_json.append(a[i]['ids'])
    # print(len(result_json))
    return result_json

def get_pages_by_id(id, urlencode_subject):
    url = f"https://advanced.fenqubiao.com/Journal/Detail/{id}"
    headers = {
    "User-Agent": USER_AGENT,
    "Connection":"keep-alive",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": COOKIE,
    "Host":"advanced.fenqubiao.com",
    "Referer":f"https://advanced.fenqubiao.com/Macro/Journal?name={urlencode_subject}&year={year}",
    }
    
    r = requests.get(url=url, headers=headers)
    # print(r.text)
    return r.text

def get_style_classes(text):
    
    soup = BeautifulSoup(text, "lxml")
    
    styles = soup.find("style")
    re1 = re.findall("[a-z][0-9]", styles.get_text())
    re2 = re.findall("\'[0-9]\'", styles.get_text())
    #print(re1)
    for i in range(len(re2)):
        re2[i] = re2[i][1]
    #print(re2)
    res = {}
    for i in range(len(re2)):
        res[re1[i]] = re2[i]
    return res

def get_info(t, subject):
    style_classes = get_style_classes(t)
    soup = BeautifulSoup(t, "lxml")
    tb1 = soup.findAll("table")[0] 
    tb2 = soup.findAll("table")[1] # 包含大类小类的分区，比较难归类
    info = {}
    for i in range(5):
        tr = tb1.find_all("tr")[i]
        name = tr.find_all("td")[0].get_text()
        value = tr.find_all("td")[1].get_text()  
        info[name] = value  
    tb2_tr = tb2.find_all("tr")
    res = {}
    lowest = 0
    for i in range(len(tb2_tr)):
        if i == 0:
            continue
        tb2_tr_td = tb2_tr[i].findAll("td")
        section,rank = None,None
        for j in range(len(tb2_tr_td)):
            
            if tb2_tr_td[j].a !=  None:
                # print(tb2_tr_td[j].a.get_text())
                section = tb2_tr_td[j].a.get_text()
            if tb2_tr_td[j].span != None:
                # print(tb2_tr_td[j].span['class'][0])
                rank = tb2_tr_td[j].span['class'][0]
                if lowest < int(style_classes[rank]):
                    lowest = int(style_classes[rank])
        res[section] = style_classes[rank]
        # print("==========")
    info["分区"] = int(res[subject])
    info["最低档"] = lowest
    info["学科信息"] = res
    return info

for key,value in subjects.items():
    if not os.path.exists(f"{path}/{key}.json"):
        json_exist = False
        break

# get_n_save_jsons.py
if not json_exist:
    os.makedirs(path, exist_ok=True)
    for key,value in subjects.items():
        subject_page = "https://advanced.fenqubiao.com/Macro/PageData"
        subject_data = {
            "draw":1,
            "start":0,
            "length":20,
            "search[value]":"",
            "search[regex]":False,
            "name": "",
            "year": -1
        }
        subject_data["name"] = key # visit subject_page to get accurate number of journals
        subject_data["year"] = year # use pre-defined year
        r = requests.post(url=subject_page,headers=headers, data=subject_data) # post with only data field
        a = loads(r.text) # convert string to json
        total = a['recordsTotal']
        subject_data["length"] = total
        r = requests.post(url=subject_page,headers=headers, data=subject_data)
        a = loads(r.text)
        formatted_json = dumps(a['data'], indent=4)
        with open(f"{path}/{key}.json", mode='w',encoding='utf-8') as f:
            f.write(formatted_json)
        print(f"key={key}, value={total}") # print subjects to check 

# get_zky_journals.py
columns=["刊名","中科院ID","年份","分区","ISSN","综述","开放","最低档","学科信息"]
os.makedirs(final_path, exist_ok=True)
for key,value in subjects.items():
    res_csv = []
    result_json = read_json(path, key)
    for i in range(len(result_json)):
        zky_journal_id = result_json[i] 
        t = get_pages_by_id(zky_journal_id, quote(key))
        info = get_info(t, key)
        info["id"] = zky_journal_id
        # 制作视图，重新整理数据
        issn = ""
        if int(year) == 2025:
            issn = info["ISSN / EISSN"].split(" / ")[0]
        else:
            issn = info["ISSN"]
        oa = ""
        if int(year) == 2025:
            oa = info["OA Journal Index（OAJ）"]
        else:
            oa = info["Open Access"]
        csv = [info["刊名"],info["id"],int(info["年份"]),info["分区"],issn,info["Review"],oa,info["最低档"],info["学科信息"]]
        res_csv.append(csv)
        print(csv)
    res_csv = pd.DataFrame(res_csv, columns=columns)
    print(res_csv.head())
    res_csv.to_excel(f"{final_path}/中科院{year}升级版_{SUBJECT}.xlsx", index=False)
