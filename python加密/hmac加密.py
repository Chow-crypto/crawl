import hmac
# 需要找到网站的key，再进行md5,sha加密
md5 = hmac.new(b'secret', b'i love you', digestmod='MD5')  # sha1
md5.update(b'123')
print(md5.hexdigest())