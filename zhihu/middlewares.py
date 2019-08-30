# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from logging import getLogger

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC


class SeleniumMiddleware():
    def __init__(self,timeout=None,service_args=[]):
        self.logger = getLogger(__name__)
        self.browser = webdriver.Chrome(service_args=service_args)
        self.wait = WebDriverWait(self.browser, 20)
        self.username = '517584811@qq.com'
        self.password = '*****'

    def process_request(self,request,spider):
        if request.url == 'https://www.douban.com/':
            self.logger.debug('Chrome is starting')
            try:
                self.browser.get(request.url)
                iframe = self.browser.find_element_by_tag_name("iframe")
                self.browser.switch_to.frame(iframe)
                self.browser.find_element_by_xpath("/html/body/div[1]/div[1]/ul[1]/li[2]").click()
                time.sleep(1)
                self.browser.find_element_by_xpath('//*[@id="username"]').send_keys(self.username)
                time.sleep(1)
                self.browser.find_element_by_xpath('//*[@id="password"]').send_keys(self.password)
                time.sleep(1)
                self.browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[5]').click()
                time.sleep(5)
                # cookies = self.browser.get_cookies()
                # print("----", cookies)
                # cookie_dict = {}
                # for cookie in cookies:
                #     cookie_dict[cookie['name']]=cookie['value']
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,'#db-isay')))
                return HtmlResponse(url=request.url,
                                    body=self.browser.page_source, request=request, encoding='utf-8',
                                    status=200)
            except TimeoutException:
                return HtmlResponse(url=request.url, status=500, request=request)


    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   service_args=crawler.settings.get('CHROME_SERVICE_ARGS'))

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


    def __del__(self):
        self.browser.close()

# self.browser.find_elements_by_xpath("//*[@id='root']/div/main/div/div/div[1]/div/form/div[1]/div")[1].click()
# self.browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(self.username)
# self.browser.find_element_by_css_selector(".SignFlow-password input").send_keys(self.password)
# self.browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()