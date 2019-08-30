"""
    author : Liuwj 
    email  : cuohohoh@gmail.com
    time   : 2019/8/29 18:12
    file   : zhihu_login.py
"""
import re

import requests

header = {
    "HOST":"www.zhihu.com",
    "Referer": "https://www.zhizhu.com",
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'
}

def get_xsrf():
    response = requests.get("https://www.zhihu.com", headers=header)
    print(response.text)
    match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text)
    if match_obj:
        return (match_obj.group(1))
    else:
        return ""

get_xsrf()