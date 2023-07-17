import requests,json,re
import pandas as pd

def crawl(qid,start, end):
    headers = {
        "authority": "www.webofscience.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en,zh;q=0.9,zh-CN;q=0.8",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://www.webofscience.com",
        "pragma": "no-cache",
        "referer": "https://www.webofscience.com/wos/woscc/summary/56b68671-dd7c-46e6-8496-40603cdfa4ab-8761dd52/relevance/1(overlay:export/exp)",
        "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "x-1p-wos-sid": "USW2EC0C547Zc7X5Aqf3seuukiCnV"
    }

    url = "https://www.webofscience.com/api/wosnx/indic/export/saveToFile"
    data = {
        "parentQid": qid,
        "sortBy": "relevance",
        "displayTimesCited": "true",
        "displayCitedRefs": "true",
        "product": "UA",
        "colName": "WOS",
        "displayUsageInfo": "true",
        "fileOpt": "othersoftware",
        "action": "saveToFieldTagged",
        "markFrom": str(start),
        "markTo": str(end),
        "view": "summary",
        "isRefQuery": "false",
        "locale": "zh_CN",
        "fieldList": [
            "AUTHORS",
            "TITLE",
            "SOURCE",
            "ABSTRACT",
            "AFFILIATIONS",
            "KEYWORDS",
            "CITTIMES",
        ],
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers,data=data)
    print(data)
    print(response.text)
    lis = response.text.split('\nPT')
    return lis

def main(qid,sum):
    results = []
    if sum%1000 == 1:
        sum+=1
    for i in range(0,sum,1000):
        end = i+1000
        if i+1000 >= sum:
            end = sum
        print(f'正在爬取{i+1}-{end}篇,wait...')
        results.extend(crawl(qid,i+1,end))
        print('完成!')

    # 处理导出的数据结果并保存
    res = []
    for i in results:
        try:# 可能没有标题，跳过
            title = re.findall(r'TI (.*?)\n[A-Z]',i,re.DOTALL)[0].replace('\n   ',' ')
        except:
            continue
        try: # 可能没有作者
            author = re.findall(r'AU (.*?)\n[A-Z]',i,re.DOTALL)[0].split('\n')[0]
        except Exception as e:
            author = ''
        try: # 可能没有期刊来源
            source = re.findall(r'SO (.*?)\n[A-Z]',i,re.DOTALL)[0]
        except Exception as e:
            source = ''
        try: # 可能没有机构
            affiliation = re.findall(r'AF (.*?)\n[A-Z]',i,re.DOTALL)[0].split('\n')[0]
        except Exception as e:
            affiliation = ''
        try: # 可能没有摘要
            abstract = re.findall(r'AB (.*?)\n[A-Z]',i,re.DOTALL)[0]
        except Exception as e:
            abstract = ''
        try:  # 可能没有关键词
            keywords = re.findall(r'DE (.*?)\n[A-Z]',i,re.DOTALL)[0]
        except Exception as e:
            keywords = ''
        try: # 可能没有年份
            year = re.findall(r'PY (.*?)\n[A-Z]',i,re.DOTALL)[0]
        except Exception as e:
            year = ''
        try: # 可能没有被引次数
            citations = re.findall(r'TC (.*?)\n[A-Z]',i,re.DOTALL)[0]
        except Exception as e:
            citations = ''
        # print(f"Title: {title}\nSource: {source}\nAuthor: {author}\nKeywords: {keywords}\nAbstract: {abstract}\nAffiliation: {affiliation}\nYear: {year}\nMonth: {month}\n")
        res.append([title,author,source,affiliation,year,abstract,keywords,citations])
    df = pd.DataFrame(res,columns=['篇名','作者','期刊来源','所在机构','文章年份','文章摘要','关键词','被引频次'])
    print(df)
    df.to_csv(f"./文献集/WOS文献信息.csv",index=False)
    df.to_excel(f".文献集/WOS文献信息.xlsx",index=False)

if __name__ == '__main__':
    main('457134a2-1118-435e-9d62-0490c13d233d-94ecef8a',75)  # 社会网络 or 社会资本
    # main('56b68671-dd7c-46e6-8496-40603cdfa4ab-8761dd52',686)  # venture capital and social network