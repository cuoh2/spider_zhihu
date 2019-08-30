"""
    author : Liuwj 
    email  : cuohohoh@gmail.com
    time   : 2019/8/29 18:36
    file   : douban.py
"""
import time

from scrapy.spiders import CrawlSpider, Rule
from scrapy import Spider, Request
from scrapy.linkextractors import LinkExtractor

from zhihu.items import DoubanUserItem


class DoubanspiderSpider(CrawlSpider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://www.douban.com/']

    rules=(
        Rule(LinkExtractor(allow=(r'^https://www.douban.com/people/.+/$'),),callback='parse_user'),
        Rule(LinkExtractor(allow='https://www.douban.com/'),callback='parse')
    )


    def start_requests(self):
        yield Request(url=self.start_urls[0], callback=self.parse, dont_filter=True)

    def parse(self, response):
        user_urls = response.css('a::attr(href)').extract()
        user_urls = filter(lambda x:True if 'people' in x
                                        and x.startswith('https')
                                        and not 'status' in x
                                        else False,user_urls)
        user_urls = list(set(user_urls))
        for user_url in user_urls:
            yield Request(url=user_url, callback=self.parse_user, dont_filter=True)

    def parse_user(self,response):
        user_item = DoubanUserItem()
        user_item['name'] = ''.join(response.xpath('//*[@id="db-usr-profile"]/div[2]/h1/text()').extract()).strip()
        user_item['bio'] = ''.join(response.xpath('//*[@id="intro_display"]/text()').extract()).strip()
        user_item['add'] = ''.join(response.xpath('//*[@id="profile"]/div/div[2]/div[1]/div/a/text()').extract()).strip()
        user_item['time'] = ''.join(response.xpath('//*[@id="profile"]/div/div[2]/div[1]/div/div/text()[2]').extract()).strip()
        print(user_item)
        time.sleep(3)
