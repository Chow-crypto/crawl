import requests,time,threading
import re as reg
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree
from concurrent.futures.thread import ThreadPoolExecutor
import warnings
warnings.filterwarnings('ignore')

def crawl(*keywords,Logic=1,get_page_num=False,current_page=1,expert=False):
    global results,lock  #全局变量，给多线程上锁，防止资源共享出问题
    # 生成查询语句
    ChildItems = [
        {
                "Key": "input[data-tipid=gradetxt-1]",
                "Title": "主题",
                "Logic": 0,
                "Items": [{
                    "Key": "",
                    "Title": keywords[0],
                    "Logic": 1,
                    "Name": "SU",
                    "Operate": "%=",
                    "Value": keywords[0],
                    "ExtendType": 1,
                    "ExtendValue": "中英文对照",
                    "Value2": ""
                }],
                "ChildItems": []
            },
    ]
    for i,key in enumerate(keywords[1:]):
        ChildItems.append(
            {
                "Key": f"input[data-tipid=gradetxt-{i+2}]",
                "Title": "主题",
                "Logic": Logic,
                "Items": [{
                    "Key": "",
                    "Title": key,
                    "Logic": 1,
                    "Name": "SU",
                    "Operate": "%=",
                    "Value": key,
                    "ExtendType": 1,
                    "ExtendValue": "中英文对照",
                    "Value2": ""
                }],
                "ChildItems": []
            })
    # print(data)
    if expert==False:
        data = {
        "IsSearch": "false",
        "QueryJson": str({
        "Platform": "",
        "DBCode": "CFLQ",
        "KuaKuCode": "",
        "QNode": {"QGroup": [{"Key": "Subject","Title": "","Logic": 4,"Items": [],"ChildItems": ChildItems},{"Key": "ControlGroup","Title": "","Logic": 1,"Items": [],"ChildItems": []}]},"CodeLang": ""}),
        "PageName": "AdvSearch",
        "DBCode": "CFLQ",
        "CurPage": current_page,
        "RecordsCntPerPage": "20",
        "CurDisplayMode": "listmode",
        "CurrSortField": "",
        "CurrSortFieldType": "desc",
        "IsSortSearch": "false",
        "IsSentenceSearch": "false",
        "Subject": ""
    }
    else:
                data={
    "IsSearch": 'false',
    "QueryJson": '{"Platform":"","DBCode":"CFLQ","KuaKuCode":"","QNode":{"QGroup":[{"Key":"Subject","Title":"","Logic":4,"Items":[{"Key":"Expert","Title":"","Logic":0,"Name":"","Operate":"","Value":"'+keywords[0]+'","ExtendType":12,"ExtendValue":"中英文对照","Value2":"","BlurType":""}],"ChildItems":[]},{"Key":"ControlGroup","Title":"","Logic":1,"Items":[],"ChildItems":[]}]},"CodeLang":""}',
    "PageName": 'AdvSearch',
    "DBCode": 'CFLQ',
    "KuaKuCodes": '',
    "CurPage": current_page,
    "RecordsCntPerPage": '20',
    "CurDisplayMode": 'listmode',
    "CurrSortField": '',
    "CurrSortFieldType": 'desc',
    "IsSortSearch": 'false',
    "IsSentenceSearch": 'false',
    "Subject": '',
    }

    headers = {
    "Accept": "text/html, */*; q=0.01",
    "Accept-Language": "en,zh;q=0.9,zh-CN;q=0.8",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://kns.cnki.net",
    "Referer": "https://kns.cnki.net/kns8/AdvSearch?dbprefix=CFLS&&crossDbcodes=CJFQ%2CCDMD%2CCIPD%2CCCND%2CCISD%2CSNAD%2CBDZK%2CCCJD%2CCCVD%2CCJFN",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\""
    }
    response = requests.post("https://kns.cnki.net/kns8/Brief/GetGridTableHtml", headers=headers, data=data)
    html_content = response.text
    with open('test.html','w',encoding='utf-8') as f:
        f.write(html_content)
    soup = BeautifulSoup(html_content, "html.parser")

    # 找到所有论文页数
    if get_page_num==True:
        print(soup.find('div',id='countPageDiv').span.text)  # 结果总数
        total=int(reg.findall(r'\d+',soup.find('div',id='countPageDiv').span.text.replace(',',''))[0])
        if total%20==0:  # 整数，刚好
            page_num = total//20
        else:
            page_num = (total//20)+1
        return page_num
    print('x'*15,f'开始爬第{current_page}页','x'*15)
    # 找到所有论文条目
    soup = etree.HTML(response.text)
    articles = soup.xpath('//tr')
    re = []
    for article in articles[1:]:
        title_tag = ''.join(article.xpath('.//a[@class="fz14"]//text()')).strip()
        if title_tag:
            title = ''.join(article.xpath('.//a[@class="fz14"]//text()')).strip()
            print(title)
            author = article.xpath('.//a[@class="KnowledgeNetLink"]//text()')[0]
            original_link = "https://kns.cnki.net" + article.xpath('.//a[@class="fz14"]/@href')[0]
            print(original_link) #title_tag["href"]
            pub_date = ''.join(article.xpath('.//td[@class="date"]//text()')).strip()
            # 提取被引频次
            try:
                citations =  int(article.xpath('.//td[@class="quote"]/a/text()')[0].strip())
            except Exception as error:
                citations=0
            # re.append((title,original_link,authors, source,issue,pub_date, institutions, abstract, keywords))
            re.append((title,author,original_link,pub_date,citations))
        else : 
            continue
    
    # 上锁，防止多线程写入冲突
    with lock:
        results.extend(re)
    

    
def crawl_detail(url):
    global results_detail,lock  #全局变量，给多线程上锁，防止资源共享出问题
    html = requests.get(url,allow_redirects=True).text
    soup = BeautifulSoup(html, "html.parser")
    top_tip = soup.find("div", class_="top-tip").span.find_all("a")
    source = top_tip[0].text
    issue = top_tip[1].text


    # 提取所在机构
    institutions = [institution.text for institution in soup.find_all("a", class_="author")]
    if institutions:
        institution = reg.sub('\d+','',reg.sub(r'\.', '', institutions[0],)).strip()
    else:
        institution = ""
    # 提取文章摘要
    try:
        abstract = soup.find("span", id="ChDivSummary").text
    except Exception as error:
        abstract = ""

    # 提取关键词
    try:
        keywords = [keyword.text.strip()[:-1] for keyword in soup.find("p", class_="keywords").find_all("a")]
        keywords = ','.join(keywords)
    except Exception as error:
        keywords = ""
    
    

    with lock:
        results_detail.append([url,[source, institution, abstract, keywords]])

def main(*keywords,Logic=1,expert=False):
    '''
    *keywords:搜索关键词
    Logic=1:并且,Logic=2:或者,Logic=3:并且非
    get_page_num:是否获取总页数
    current_page:当前页数
    '''
    global results,results_detail,lock
    results = [];results_detail = []
    lock = threading.Lock()
    # 第一步，获取所有文章
    try:
        page_num = crawl(*keywords,Logic=Logic,get_page_num=True,expert=expert)
        print(f'共有{page_num}页')
    except Exception as e:
        print('未搜索到结果！',e)
        return
    with ThreadPoolExecutor(max_workers=10) as executor:
        for page in range(1,page_num+1):
            executor.submit(crawl,*keywords,Logic=Logic,current_page=page,expert=expert)
            time.sleep(0.5)  # 强制休息放慢速度

    # 第二步，获取文章摘要等详情信息
    df = pd.DataFrame(results)
    df.columns = ['篇名','作者','原始链接','公开日期','被引频次']
    urls = df.原始链接
    with ThreadPoolExecutor(max_workers=20) as executor:  #20个线程爬
        for url in urls:
            executor.submit(crawl_detail,url)
    results_detail = dict(results_detail)
    df[['期刊来源','所在机构','文章摘要','关键词']] = df.apply(lambda x:pd.Series(results_detail.get(x.原始链接)), axis=1)

    # 第三步 存储
    df.公开日期=pd.to_datetime(df.公开日期)
    df['文章年份'] = df.公开日期.dt.year
    df=df.sort_values(by='公开日期',ascending=False)
    df = df[['篇名', '作者', '期刊来源', '所在机构', '原始链接','文章年份', '文章摘要', '关键词','被引频次']]
    df.to_csv(f"./文献集/知网文献信息{keywords}.csv",index=False)
    # df.to_excel(f"知网文献信息.xlsx",index=False)

if __name__ == '__main__':
    main('区域产业空间布局','技术',Logic=1)  # 逻辑与