# 生成中国所有省份和城市的列表
import requests
from concurrent.futures.thread import ThreadPoolExecutor
import PyPDF2
import jieba
from collections import Counter

#  读取企业简称名单
with open('/Users/nanapower/学习资料/python_learnning/模块与项目/AI/图灵AI/巨潮资讯/年报爬取/企业简称名单.txt','w') as f:
    f.write(company_list)