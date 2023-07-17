import requests, execjs, hashlib,re,pprint,tqdm,json,time
def get_data(keyword,page):
    # 获取拼接字符串
    jscode = '''
    function x(keyword,page){
        var n = ""
            ,y = '$d6eb7ff91ee257475%'
            ,d = keyword
            ,t= (new Date).getTime()
            , i = 16
            , a = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"];
        for (var o = 0; o < i; o++) {
            n += a[Math.round(Math.random() * (a.length - 1))]
        }
        return [[y,10,page,t,n,keyword].sort().join(""), t, n]
    }
    '''
    code,ts,rs = execjs.compile(jscode).call('x',keyword,page)
    sha1 = hashlib.sha256()
    sha1.update(code.encode('utf-8'))
    params = {
        'ts': ts,
        'rs': rs,
        'signature': sha1.hexdigest(),
        'keywords': keyword,
        'page_size': 10,
        'page' : page
    }

    url = 'https://tousu.sina.com.cn/api/index/s'
    # 请求数据
    return requests.get(url,params=params)
def main(keyword):
    response = get_data(keyword,1)
    page_amount,item_count=re.findall('page_amount":(\d+).*"item_count":(\d+)',response.text)[0]
    print('总页数:',page_amount,'总数',item_count)

    data = []
    for page in tqdm.trange(40):
        response = get_data(keyword,page+1)
        for i in response.json()["result"]["data"]["lists"]:
            title = i["main"]["title"]
            summary = i["main"]["summary"]
            data.append(({'title':title,'summary':summary}))
    # 数据清理
    data = re.sub('<span.*?">','',str(data))
    data = {'data':eval(re.sub('</span>','',str(data)))}
    with open(f'黑猫投诉--{keyword}.json','wt',encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False)
    print(data)

if __name__ == '__main__':
    start = time.time()
    main('淘宝')
    print(f'用时{time.time()-start}秒')
