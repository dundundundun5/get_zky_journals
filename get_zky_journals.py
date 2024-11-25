# "勤换cookie"
import json
import os
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('--year', default='2019', choices=['2019', '2020', '2021', '2022', '2023'])
args = parser.parse_args()
YEAR = args.year
FINAL_PATH = f"./excel_{YEAR}/"
SUBJECTS_2019 = {"地球科学":449,
            "物理与天体物理":307,
            "数学":508,
            "农林科学":675,
            "材料科学":373,
            "计算机科学":528,
            "环境科学与生态学":374,
            "化学":389,
            "工程技术":1121,
            "生物学":877,
            "医学":3499,
            "综合性期刊":56,
            "心理学":489,
            "教育学":238,
            "经济学":403,
            "管理学":405,
            }
SUBJECTS_2020 = {"地球科学":458,
            "物理与天体物理":317,
            "数学":518,
            "农林科学":683,
            "材料科学":395,
            "计算机科学":529,
            "环境科学与生态学":382,
            "化学":398,
            "工程技术":1156,
            "生物学":885,
            "医学":3601,
            "综合性期刊":60,
            "心理学":491,
            "教育学":251,
            "经济学":414,
            "管理学":420,
            }
SUBJECTS_2021 = {"地球科学":464,
            "物理与天体物理":320,
            "数学":532,
            "农林科学":689,
            "材料科学":412,
            "计算机科学":518,
            "环境科学与生态学":394,
            "化学":405,
            "工程技术":1163,
            "生物学":920,
            "医学":3672,
            "综合性期刊":61,
            "心理学":497,
            "教育学":255,
            "经济学":414,
            "管理学":420,
            }
SUBJECTS_2022 = {"地球科学":470,
            "物理与天体物理":323,
            "数学":543,
            "农林科学":702,
            "材料科学":410,
            "计算机科学":524,
            "环境科学与生态学":400,
            "化学":403,
            "工程技术":1183,
            "生物学":917,
            "医学":3722,
            "综合性期刊":63,
            "法学":858,
            "心理学":490,
            "教育学":260,
            "经济学":420,
            "管理学":423,
            "人文科学":444
            }
SUBJECTS_2023 = {"地球科学":470,
            "物理与天体物理":323,
            "数学":558,
            "农林科学":725,
            "材料科学":371,
            "计算机科学":501,
            "环境科学与生态学":388,
            "化学":389,
            "工程技术":1032,
            "生物学":940,
            "医学":3773,
            "综合性期刊":63,
            "社会学":1029,
            "心理学":488,
            "教育学":267,
            "经济学":413,
            "管理学":429,
            "哲学":416,
            "历史学":414,
            "文学":580,
            "艺术学":241
            }
SUBJECTS = eval(f"SUBJECTS_{YEAR}")


SUBJECT = ""
urlencode_subject = ""
PATH = f"./json_{YEAR}"

def read_json(path, subject):
    f = open(f'{path}/{subject}.json', 'r')
    content = f.read()
    a = json.loads(content)
    result_json = []
    for i in range(len(a)):
        result_json.append(a[i]['Id'])
    # print(len(result_json))
    return result_json

def get_pages_by_id(id):
    url = f"https://advanced.fenqubiao.com/Journal/Detail/{id}"
    headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36 Edg/131.0.0.0",
    "Connection":"keep-alive",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "Hm_lvt_0dae59e1f85da1153b28fb5a2671647f=1709621250; auth=03E1C63F44A18CFCB7A0B30E70EEDF07BDDDC36783433250635AD9833E212EB5305CFC88FFC631869BB6371BAEF05A177C512E544057C60AE26F35EAE5013E84E759A1922A624D3DD9F3A6B297BBE5F3557E1439F551F660A7F766ECE43228CDBD63BCBD75B83BF9010D060A4C5EAB9F05ACF60629CAED29204FA5BC4533499CC3ED5E128BCBF9CCA75B848FF4E43370D2FD14CAB908873E934C56FD489F155573DD81D4BD7BE708474D7FCC87A8414F10E14DE6540E7444154FA7749D3606AD5059020343C6D7669ACA6A10488357CEF9234AA5D4D58FEDEAE5584B56645E6B76C96E3418B10A295B4C450CB762930E9EF238EC0562738B63DEA4BB0AC0C16CD41DB6E17C302ADD81BB938F36FCA4780D2BF58F1C84D183BB88B6EBBBAF0FA51E00693DB9ACF74BCAC2A68138C76AE9B0B74D9522F479B6A686BBA5C492834BC37C3AE6763E62B065E5F273A8FD390CFE070B58924449818B63BD6BEE7143080F082FA0FF80AD886EE939F34159D11E0FA72FCF21DEC1C1732E3CE077662CEFF933360D394E63B09E6D76FE4A485963E2B9CB2BA10B67EF9E23E0AD5CFFCCD0127DE4C4864D4A0A9B8FC1710205BF90C1346FED3DE69823DDD3592DD045E38DB75767E9DCFC8B0E50D95BF17E2E88EA; Hm_lvt_7e6e274f8fab6425c743106cbd2e8d99=1732014711; HMACCOUNT=1625AD0AAC316688; Hm_lpvt_7e6e274f8fab6425c743106cbd2e8d99=1732017307",
    "Host":"advanced.fenqubiao.com",
    "Referer":f"https://advanced.fenqubiao.com/Macro/Journal?name={urlencode_subject}&year={YEAR}",
    }
    import requests
    r = requests.get(url=url, headers=headers)
    # print(r.text)
    return r.text

def get_style_classes(text):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(text, "lxml")
    
    styles = soup.find("style")
    import re
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

def get_info(t):
    style_classes = get_style_classes(t)
    from bs4 import BeautifulSoup
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
    info["分区"] = int(res[SUBJECT])
    info["最低档"] = lowest
    info["学科信息"] = res
    return info
if __name__ == '__main__':

    import pandas as pd
    columns=["刊名","中科院ID","年份","分区","ISSN","综述","开放","最低档","学科信息"]
    import os
    os.makedirs(FINAL_PATH, exist_ok=True)
    for key,value in SUBJECTS.items():
        res_csv = []
        SUBJECT = key
        result_json = read_json(PATH, SUBJECT)
        for i in range(len(result_json)):
            zky_journal_id = result_json[i] - 9
            t = get_pages_by_id(zky_journal_id)
            info = get_info(t)
            info["id"] = zky_journal_id
            # 制作视图，重新整理数据
            csv = [info["刊名"],info["id"],int(info["年份"]),info["分区"],info["ISSN"],info["Review"],info["Open Access"],info["最低档"],info["学科信息"]]
            res_csv.append(csv)
            print(csv)
        res_csv = pd.DataFrame(res_csv, columns=columns)
        print(res_csv.head())
        res_csv.to_excel(f"{FINAL_PATH}/中科院{YEAR}升级版_{SUBJECT}.xlsx", index=False)
        
