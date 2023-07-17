import requests
from multiprocessing import Pool, set_start_method
from concurrent.futures.thread import ThreadPoolExecutor
import pandas as pd
import os
company_list = pd.read_excel('/Users/nanapower/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/0a5ee70a49025e211f9ccc484a9c8ff4/Message/MessageTemp/27ba9480ba2304984c4a1e9a4793d843/File/企业id获取结果.xlsx')
id = list(zip(company_list.全称,company_list.secCode,company_list.orgId))
import time
# 功能二
def select(code, orgid):
    time.sleep(0.2)
    # 获取报告类型
    category="category_ndbg_szsh;"

    # 获取时间
    start = '2011-01-01'
    end = '2023-04-21'

    # 根据股票代码的头文字，判断股票交易所信息
    if str(code)[0] == '6':
        column = 'sse'
        plate = 'sh'
    elif str(code)[0] == '8' or str(code)[0] == '4':
        column = 'third'
        plate = 'neeq'
    else:  # 3 0
        column = 'szse'
        plate = 'sz'

    # 设置初始页码
    page_num = 1
    # 设置初始列表存储筛选结果
    pdf_list = []
    while True:
        # 设置报告筛选参数
        params = {
            'stock': '{},{}'.format(code, orgid),
            'tabName': 'fulltext',
            'pageSize': '30',
            'pageNum': str(page_num),
            'category': '',#category,
            'seDate': '{}~{}'.format(start, end),
            'column': column,
            'plate': plate,
            'searchkey': '',
            'secid': '',
            'sortName': '',
            'sortType': '',
            'isHLtitle': ''
        }

        # 发起报告搜索请求
        r = requests.post('http://www.cninfo.com.cn/new/hisAnnouncement/query', params=params)
        try:
            r_json = r.json()
        except:
            print(code,'error')
            print(r.text)
        # 判断是否搜索失败、或者无搜索结果，如果无结果则结束
        if r_json['announcements'] == None or len(r_json['announcements']) == 0:
            return  [['无搜索结果！','无搜索结果！']]
        # 遍历搜索结果
        for i in r_json['announcements']:
            pdf_list.append([i['announcementTitle'], 'http://static.cninfo.com.cn/'+i['adjunctUrl']])
        # print(type(r_json['hasMore']))
        # 判断是否还有下一页数据，没有的话就结束循环
        if r_json['hasMore'] != True:
            break
        # 如果有的话，让页数加一，开始下一轮循环
        page_num += 1
    return pdf_list

def run(index,name,code, orgid):
    lis = select(code, orgid)
    if lis == [['无搜索结果！','无搜索结果！']]:
        with open(f'/Users/nanapower/学习资料/python_learnning/模块与项目/AI/图灵AI/巨潮资讯/年报爬取/pdf未处理/!{index}_{name}.txt','w') as f:
            for i in lis:
                f.write(i[0]+' ')
                f.write(i[1]+'\n')
            return
    with open(f'/Users/nanapower/学习资料/python_learnning/模块与项目/AI/图灵AI/巨潮资讯/年报爬取/pdf未处理/{index}_{name}.txt','w') as f:
        for i in lis:
            f.write(i[0]+' ')
            f.write(i[1]+'\n')
    print(index,'下载完成！')
if __name__ == '__main__':
    # set_start_method('fork')
    lis = os.listdir('/Users/nanapower/学习资料/python_learnning/模块与项目/AI/图灵AI/巨潮资讯/年报爬取/pdf未处理/')
    lis = [i.split('_')[0] for i in lis]
    pool = Pool(processes=8)
    for index,i in enumerate(id):
        # time.sleep(0.3)
        if str(index+1) in lis:
            print(str(index+1),'已下载！')
            continue
        run(index+1,i[0],i[1],i[2])
        pool.apply_async(run,(index+1,i[0],i[1],i[2]))
    pool.close()  # 关闭进程池，关闭之后，不能再向进程池中添加进程
    pool.join()
    # with ThreadPoolExecutor(10) as pool:
    #     for index,i in enumerate(id):
    #         if str(index) in lis:
    #             print(str(index),'已下载！')
    #             continue
    #         pool.submit(run,index+1,(i[0],i[1],i[2]))