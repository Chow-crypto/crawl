import hashlib, time, random, math
import requests

# 加密有头部Cookie',Referer,User-Agent 请求参数bv， lts， sign，salt
class Crawl():
    def __init__(self):
        self.version = "5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        self.headers = {
            'Cookie': 'OUTFOX_SEARCH_USER_ID=-120181295@10.110.96.158; OUTFOX_SEARCH_USER_ID_NCOO=1458853935.5657043; ___rl__test__cookies={}'.format(time.time()),
            'Referer': 'https://fanyi.youdao.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        }

    def md5(self,key):
        industry = hashlib.md5()
        industry.update(key.encode())
        return industry.hexdigest()

    def spider(self,word):
        bv = self.md5(self.version)
        lts = str(math.ceil(time.time()*1000)) + str(random.randint(1,10))
        key = "fanyideskweb" + word + lts + "Ygy_4c=r#e#4EX^NUGUc5"
        sign = self.md5(key)
        # print(salt)
        # print(sign)
        # print(lts)
        # print(bv)
        url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        data = {
            'i': word,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': lts,
            'sign': sign,
            'lts': lts[:-1],
            'bv': bv,
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTlME',
            }
        
        res = requests.post(url, data=data, headers=self.headers).json()
        data = res.get('translateResult')
        msg = []
        if res.get('errorCode') == 0:
            for i in data:
                for t in i:
                    print(t['src'])  # 中文
                    print(t['tgt'])  # 英文
                    msg.append(t['src'])
                    msg.append(t['tgt'])
        return '\n'.join(msg)
# with open('new.txt',) as f:     文章翻译
#     word = f.read()
if __name__ == '__main__':
    while True:
        word =input('请输入要翻译的句子：')
        if word == 'q':
            print('程序结束！')
            break
        print('翻译结果:')
        Crawl().spider(word)
