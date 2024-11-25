# "每天勤换Cookie"
import requests
from argparse import ArgumentParser
from .zky_properties import COOKIE,USER_AGENT
parser = ArgumentParser()
parser.add_argument('--year', default='2019', choices=['2019', '2020', '2021', '2022', '2023'])
args = parser.parse_args()
YEAR = args.year
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
PATH =f"./json_{YEAR}"


params = {
    "start":1,
    "length":-1
}
data = {
    "name":"None",
    "type":"zky",
    "keyword":"",
    "year":YEAR
}
url = "https://advanced.fenqubiao.com/Macro/GetJson"
headers = {
    "User-Agent": USER_AGENT,
    "Connection":"keep-alive",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": COOKIE,
    "Host":"advanced.fenqubiao.com",
    }
import os
os.makedirs(PATH, exist_ok=True)
for key,value in SUBJECTS.items():
    params['length'] = value # 要爬多少条期刊
    data["name"] = key
    data["year"] = YEAR
    r = requests.post(url=url,headers=headers, params=params, data=data)
    with open(f"{PATH}/{key}.json", mode='w',encoding='utf-8') as f:
        f.write(r.text)
