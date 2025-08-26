import pandas as pd
import json
from argparse import ArgumentParser
from zky_properties import *
parser = ArgumentParser()
parser.add_argument('--year', default='2025', choices=['2019', '2020', '2021', '2022', '2023', '2025'])
args = parser.parse_args()
year = args.year

def a(row):
    temp = row.学科信息.replace('\'', '"')
    small = json.loads(temp)
    i = 0
    for small_k, _ in small.items():
        if i == 0:
            i += 1
            continue
        sm = small_k.split(" ")   
        row.学科 += f",{sm[-1]}"
    return row
col = ['刊名', '中科院ID', '年份', '分区', 'ISSN', '综述', '开放', '最低档', '学科信息','学科']
res = pd.DataFrame(None, columns=col)
SUBJECTS = eval(f"SUBJECTS_{year}")
for k,_ in SUBJECTS.items():

    data = pd.read_excel(f"./excel_{year}/中科院{year}升级版_{k}.xlsx")
    data['学科'] = k
    data = data.apply(a, axis=1)
        
        
    res = pd.concat([res, data], axis=0)

res.to_excel(f'中科院{year}升级版.xlsx', index=False)

