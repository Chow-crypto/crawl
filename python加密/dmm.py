# # from email import header
# # import requests
# url = 'https://www.zhipin.com/gongsi/_zzz_c101010100_s301/?page=3&ka=page-3'
# # headers = {
# #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
# #     'referer': 'https://www.zhipin.com/web/common/security-check.html?seed=0lamxKwfpDiSecHb7aMjILxG210%2Fn6LGyY3WyRmFnD443VIUdjBBHcWmeSKlKy%2BtfZrNCbOJNRjed5p%2BbEoZuw%3D%3D&name=ce475149&ts=1662607897836&callbackUrl=%2Fgongsi%2F_zzz_c101010100_s301%2F%3Fpage%3D3%26ka%3Dpage-3&srcReferer=https%3A%2F%2Fwww.zhipin.com%2Fgongsi%2F_zzz_c101010100_s301%2F%3Fpage%3D2%26ka%3Dpage-2',
# #     'cookie': 'wd_guid=cf8b3047-110a-463f-ae7b-291c0e89f1a5; historyState=state; _bl_uid=z4laL6spe3pbanypLf339Oe9qUIh; __g=-; __l=l=%2Fwww.zhipin.com%2Fweb%2Fgeek%2Fjob%3Fquery%3D%25E5%2589%258D%25E7%25AB%25AF%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588%26city%3D101210100&r=&g=&s=3&friend_source=0&s=3&friend_source=0; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1660410635,1660828986,1662459502,1662517238; __fid=b2d0fc2bd582de137ea062c67e23a9c4; __c=1662461699; __a=88548036.1653621656.1662459505.1662461699.140.13.32.140; __zp_stoken__=67f6ef3Q1Ci8FLEhQP3NjOhAYdWYaO25mYwUOVHg0UnENLHgIUF52OXkNElNDVSEwJTRYVVMjEXNPDRc9Xjl6DHsWJXAfIR9eUFARbGE8PRg7dk8MYDx3IhIyVHkedkoSHRJODQwxcQAMMV8HbVlzT3FsAUIaNFtPMkYjQCYRDl5sHFRlbDdAM39yeDJcT3gbYBtPb0F0dA%3D%3D; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1662607904'
# # }
# # re = requests.get(url, headers=headers)
# # print(re.text, re)

# import requests


# headers = {
#     "authority": "www.zhipin.com",
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#     "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
#     "cache-control": "no-cache",
#     "pragma": "no-cache",
#     "referer": "https://www.zhipin.com/web/common/security-check.html?seed=0lamxKwfpDiSecHb7aMjILxG210%2Fn6LGyY3WyRmFnD443VIUdjBBHcWmeSKlKy%2BtfZrNCbOJNRjed5p%2BbEoZuw%3D%3D&name=ce475149&ts=1662607897836&callbackUrl=%2Fgongsi%2F_zzz_c101010100_s301%2F%3Fpage%3D3%26ka%3Dpage-3&srcReferer=https%3A%2F%2Fwww.zhipin.com%2Fgongsi%2F_zzz_c101010100_s301%2F%3Fpage%3D2%26ka%3Dpage-2",
#     "sec-ch-ua": "\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"macOS\"",
#     "sec-fetch-dest": "document",
#     "sec-fetch-mode": "navigate",
#     "sec-fetch-site": "same-origin",
#     "sec-fetch-user": "?1",
#     "upgrade-insecure-requests": "1",
#     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
# }
# cookies = {
#     "wd_guid": "cf8b3047-110a-463f-ae7b-291c0e89f1a5",
#     "historyState": "state",
#     "_bl_uid": "z4laL6spe3pbanypLf339Oe9qUIh",
#     "__g": "-",
#     "__l": "l=%2Fwww.zhipin.com%2Fweb%2Fgeek%2Fjob%3Fquery%3D%25E5%2589%258D%25E7%25AB%25AF%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588%26city%3D101210100&r=&g=&s=3&friend_source=0&s=3&friend_source=0",
#     "Hm_lvt_194df3105ad7148dcf2b98a91b5e727a": "1660410635,1660828986,1662459502,1662517238",
#     "__fid": "b2d0fc2bd582de137ea062c67e23a9c4",
#     "__c": "1662461699",
#     "__a": "88548036.1653621656.1662459505.1662461699.140.13.32.140",
#     "__zp_stoken__": "67f6ef3Q1Ci8FLEhQP3NdbHkKYElfOQ0lcAUOVHg0UnENLHgIUGEpWBBKIWI1IVMeJTRYVVMjEXNPDRdrW2QhGSUwRnxjYh9eUFARbGE8PRg"
# }
# # url = "https://www.zhipin.com/gongsi/_zzz_c101010100_s301/"
# params = {
#     "page": "3",
#     "ka": "page-3"
# }
# response = requests.get(url, headers=headers, cookies=cookies, params=params)
# response.encoding = 'utf-8'
# print(response.text)
# print(response)
# lis = [1,2,3,4]
# lis1 = lis.copy()
# print([i for i in zip(lis,lis1)])
# print(locals())
import shutil
print(shutil.copy('dmm.py','./python加密'))