import requests  # 网络请求，
import os  # 文件操作
from lxml import etree  # 解析网页
from concurrent.futures.thread import ThreadPoolExecutor  # 线程池
def crawl(type,start,end):
    with ThreadPoolExecutor(10) as pool:  # 开10个线程池
        for page in range(start,end+1):
            if page == 1:
                page_url = ''
            else:
                page_url = f'_{page}'
            page_url = f'https://pic.netbian.com/{type}/index{page_url}.html'
            pool.submit(crawl_page,page_url,page)

def crawl_page(page_url,page):
    re = requests.get('https://pic.netbian.com/4kfengjing/index_3.html')
    re.encoding = re.apparent_encoding  # 自动识别网页编码（防止乱码）--即：<meta charset="gbk">
    HTML = etree.HTML(re.text)
    pic_lis = HTML.xpath('.//ul[@class="clearfix"]/li')
    pic_lis = HTML.xpath('.//ul[@class="clearfix"]/li')
    for pic in pic_lis:
        name = pic.xpath('./a/img/@alt')[0]
        link = pic.xpath('./a/img/@src')[0]
        if os.path.exists('./pic') == False:  # 如果不存在pic文件夹，则创建
            os.mkdir('./pic')
        with open(f'./pic/{name}.jpg','wb') as f:
            f.write(requests.get(f'https://pic.netbian.com{link}').content)
            print(f'{name}下载完成')
    print(f'**************第{page}页下载完成**************')

if __name__ == '__main__':
    crawl('4kfengjing',1,5)