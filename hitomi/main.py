#  线程池 + js逆向
import time, random
import requests,execjs,json,os
from concurrent.futures.thread import ThreadPoolExecutor
from multiprocessing import Pool, set_start_method
from loguru import logger
# hash = '"a1bd32e336d3ce9e0d237fa2c29b47ba0386806b61404da1cf71922613cec3e4"'
# jscode = 'function run(){\nvar m = /(..)(.)$/.exec('+hash+')\nreturn parseInt(m[2]+m[1], 16).toString(10);}'
# code = execjs.compile(jscode).call('run')
# print(code)
# with open('/Users/nanapower/Desktop/python爬虫第六期/代码.py/js逆向/hitomi/hitomi.js', 'r', encoding='utf-8') as f:
#     jscode = f.read()
# code = execjs.compile(jscode).call('url_from_url_from_hash')
# print(code)
start = time.time()
suffix = '''function subdomain_from_url(url, base) {
    var retval = 'b';
    if (base) {
            retval = base;
    }
    
    var b = 16;
    
    var r = /\/[0-9a-f]{61}([0-9a-f]{2})([0-9a-f])/;
    var m = r.exec(url);
    if (!m) {
            return 'a';
    }
    
    var g = parseInt(m[2]+m[1], b);
    if (!isNaN(g)) {
            retval = String.fromCharCode(97 + gg.m(g)) + retval;
    }
    
    return retval;
};

function url_from_url(url, base) {
    return url.replace(/\/\/..?\.hitomi\.la\//, '//'+subdomain_from_url(url, base)+'.hitomi.la/');
}


function full_path_from_hash(hash) {
    return gg.b+gg.s(hash)+'/'+hash;
}

function real_full_path_from_hash(hash) {
    return hash.replace(/^.*(..)(.)$/, '$2/$1/'+hash);
}


function url_from_hash(galleryid, image, dir, ext) {
    ext = ext || dir || image.name.split('.').pop();
    dir = dir || 'images';
    
    return 'https://a.hitomi.la/'+dir+'/'+full_path_from_hash(image.hash)+'.'+ext;
}

function url_from_url_from_hash(galleryid, image, dir, ext, base) {
    if ('tn' === base) {
            return url_from_url('https://a.hitomi.la/'+dir+'/'+real_full_path_from_hash(image.hash)+'.'+ext, base);
    }
    return url_from_url(url_from_hash(galleryid, image, dir, ext), base);
}
var gg
var ext'''


galleryid = '1589674'
header = {
    'referer': f'https://hitomi.la/reader/{galleryid}.html'
}
dir = 0
jscode = None
data = None
title = None

def get_url():
    # ## 写 js 文件
    re = requests.get('https://ltn.hitomi.la/gg.js')
    with open('/Users/nanapower/Desktop/python爬虫第六期/代码.py/js逆向/hitomi/hitomi.js','w', encoding='utf-8') as f:
        f.write(re.text)
        # gg_b = re.text[-16:-6]
        f.write(suffix)

def get_pic():
    global jscode,data,title
    with open('/Users/nanapower/Desktop/python爬虫第六期/代码.py/js逆向/hitomi/hitomi.js', 'r', encoding='utf-8') as f:
        jscode = f.read()
    re = requests.get(f'https://ltn.hitomi.la/galleries/{galleryid}.js').text[18:]  # gallery id 获取全部图片
    data = json.loads(re)['files']
    title = json.loads(re)['title']
    # 先创建保存文件
    if not os.path.exists(f'/Users/nanapower/Pictures/下载图库/Hitomi/{title}/'):
        os.mkdir(f'/Users/nanapower/Pictures/下载图库/Hitomi/{title}/')
    if not os.path.exists('/Users/nanapower/Pictures/下载图库/Hitomi'):
        os.mkdir('/Users/nanapower/Pictures/下载图库/Hitomi')

def main():
    global dir
    get_url()
    get_pic()
    # 总结：线程开多了没用
    #  线程池（100） 1.12GB 耗时366秒 平均3.13MB/s
    #  线程池（200） 2.6GB 耗时853秒 平均3.12MB/s
    #  线程池（40） 1.42GB 耗时326秒 平均4.46MB/s
    with ThreadPoolExecutor(100) as pool:
        for i in data:
            dir = i['hasavif']
            if dir:
                dir = 'avif'
            else:
                dir = "webp"
            name = i['name']
            url = execjs.compile(jscode).call('url_from_url_from_hash',galleryid,i,dir,'','a')
            pool.submit(download,url,name,dir)


    # 总结： 进程耗费系统资源
    # #进程池(8) 206MB 耗时 158秒 平均1.3MB/s
    # 进程池(50) 477MB 耗时 105秒 平均 4.5MB/s
    # 进程池(50) 1.47GB 耗时 721秒 平均 2.08MB/s(开了另一个vscode多线程)
    # 进程池(100) 477MB 耗时 105秒 平均 4.5MB/s 14:14  一百太多了 
    # set_start_method('fork') macos 需要这样设置
    # pool = Pool(processes=50)
    # for i in data:
    #     dir = i['hasavif']
    #     if dir:
    #         dir = 'avif'
    #     else:
    #         dir = "webp"
    #     name = i['name']
    #     url = execjs.compile(jscode).call('url_from_url_from_hash',galleryid,i,dir,'','a')
    #     pool.apply_async(download, (url,name,dir))
        
    # pool.close()  # 关闭进程池，关闭之后，不能再向进程池中添加进程
    # pool.join()


def download(pic_url,name,dir):
    re = requests.get(pic_url, headers = header)
    if re.status_code == 200:
        with open(f'/Users/nanapower/Pictures/下载图库/Hitomi/{title}/{name.replace(name[-3:],dir)}', 'wb') as f:
            f.write(re.content)
        logger.info(f'{name}下载完成{pic_url}')
    else:
        logger.info(re.status_code, '下载失败',pic_url)


if __name__ == '__main__':
    main()
    print('总耗时：',time.time()-start)