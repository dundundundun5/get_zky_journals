
# 爬虫说明
**(必须确认)**
1. 前提1：保证电脑有中科院数据库访问Cookie

    修改zky_properties.py中的`COOKIE`和`USER_AGENT`

1. 前提2：保证电脑有python一系列库

    `pip install beautifulsoup4 -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple`
    
    `pip install pandas -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple`

    `pip install lxml -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple`

    `pip install openpyxl -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple`

    `如果还缺就自己补一下`


## 升级版说明 (2025年更新)
中科院期刊查询接口使用方法为：期刊名-id

id号需要手动查询

通过浏览器开发者工具能从中科院2025升级版的接口里看到期刊id号是

https://advanced.fenqubiao.com/Macro/PageData

`data = {
            "draw":1,
            "start":0,
            "length":20,
            "search[value]":"",
            "search[regex]":False,
            "name": "",
            "year": -1
        }`

其中`name`是学科名称，不需要url转码

`year`就是`int`年份

~~http://advanced.fenqubiao.com/Journal/Detail/249639~~ 已失效

现在是 http://advanced.fenqubiao.com/Journal/Detail/一串字母

上方链接是一个静态网页，罗列了一个期刊的所有信息，只需变换id，即可汇总不同期刊的具体信息


## 升级版使用方法



1. 获取中科院title-id的json键值对

    `python get.py --year 填入升级版的年份`

    `默认2025年`

    `python get.py`

2. （可选）将中科院当前的所有大类excel合并为一个excel

    ```python merge.py --year 同上填入年份```


## 旧版说明(具备前提后，爬取过程可能已经失效，但是excel文件依然有效)

使用动态网页ASP.NET,每个网页的post负载都需要3个验证码才能成功相应，验证码存在于该网页源码的底部

## 旧版使用方法
1. 获取`year`+`title `

    `$i 替换成年份`
   
    ```python old_get_n_save_csvs.py --year $i --subject 地学```

    ```python old_get_n_save_csvs.py --year $i --subject 地学天文```

    ```python old_get_n_save_csvs.py --year $i --subject 工程技术``` 

    ```python old_get_n_save_csvs.py --year $i --subject 管理科学``` 

    ```python old_get_n_save_csvs.py --year $i --subject 化学```

    ```python old_get_n_save_csvs.py --year $i --subject 环境科学与生态学``` 

    ```python old_get_n_save_csvs.py --year $i --subject 农林科学``` 

    ```python old_get_n_save_csvs.py --year $i --subject 社会科学```

    ```python old_get_n_save_csvs.py --year $i --subject 生物```

    ```python old_get_n_save_csvs.py --year $i --subject 数学```

    ```python old_get_n_save_csvs.py --year $i --subject 物理``` 

    ```python old_get_n_save_csvs.py --year $i --subject 医学``` 

    ```python old_get_n_save_csvs.py --year $i --subject 综合性期刊```

1. 获取期刊条目并保存为excel

    ```python old_get_zky_journals.py --year $i```
