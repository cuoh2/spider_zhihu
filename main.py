"""
    author : Liuwj 
    email  : cuohohoh@gmail.com
    time   : 2019/8/29 18:37
    file   : main.py
"""
import os
import sys

from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#execute(["scrapy", "crawl", "douban"])
execute(["scrapy", "crawl", "zhihuspider"])