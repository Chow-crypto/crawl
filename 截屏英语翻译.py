import os, pytesseract, smtplib, time
from python加密.md5_有道 import Crawl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_path():
    #生成截图时间名称
    dic = {'Jan': 1,'Feb': 2,'Mar': 3,'Apr': 4,'May': 5,'Jun': 6,'Jul': 7,'Aug': 8,'Sep': 9,'Oct': 10,'Nov': 11,'Dec': 12}
    month, day, hour, year = time.ctime().split()[1:]
    month = str(dic.get(month))

    #得到月
    if len(month) !=2:
        month = '0'+month
    # 得到天
    if len(day) != 2:
        day = '0'+day
    hour = hour.split(':')[0]

    #得到小时
    if len(hour) != 2:
        hour = '0'+hour
    index = f'Screen Shot {year}-{month}-{day} at {hour}'


    path = os.listdir('/Users/nanapower/Desktop/')
    def f():
        for i in path:
            if i.startswith(index):
                return '/Users/nanapower/Desktop/'+i
    return f()

def get_text_by_tes(path):
    text = pytesseract.image_to_string(path, lang='eng+chi_sim')
    os.remove(path)
    return Crawl.spider(Crawl(),text)
def get_text_by_ocr(path):
    import easyocr
    reader = easyocr.Reader(['ch_sim','en'])
    text = reader.readtext(path)
    text = '\n'.join([i[1] for i in text])
    os.remove(path)
    return Crawl.spider(Crawl(),text)

def send_qq(data):
    smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)

    smtp.login('2028731463@qq.com', 'yqtfcksjfucycchf')

    content = data
    email_content = MIMEText(content, 'plain', 'utf-8')
    # with open('/Users/nanapower/Desktop/python/office/fengbian/practice_3/工作/新产品介绍.pdf', 'rb') as f:
    #     file_data = f.read()
    # attachment = MIMEText(file_data, 'base64','utf-8')
    # attachment.add_header('content-disposition','attachment',filename='新产品介绍.pdf')

    msg=MIMEMultipart()
    msg['from'] = '2028731463@qq.com'
    msg['to'] = '爱坤'
    msg['subject'] = '英语翻译'

    msg.attach(email_content)
    # msg.attach(attachment)
    smtp.sendmail('2028731463@qq.com', '2544980143@qq.com', msg.as_string())  # 叔615820006 坤2544980143
    smtp.quit()
if __name__ == '__main__':
    path = get_path()
    choice = input('请选择图像识别模块    tesseract(耗时短，质量差，大约1s)===输入1,     easyocr(耗时长，质量高，大约30s)===输入2:\n')
    if choice == '1':
        text = get_text_by_tes(path)
    if choice == '2':
        text = get_text_by_ocr(path)
    # send_qq(text)
    print('\n程序结束！')