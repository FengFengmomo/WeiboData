# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from scrapy.conf import settings
from scrapy.http import HtmlResponse
from scrapy import signals
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import chardet
import logging
import pickle

class WeibodataSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class JsAjaxHtml(object):

    def __init__(self):
        self.dcap = dict(DesiredCapabilities.PHANTOMJS)
        self.dcap['phantomjs.page.setting.userAgent'] = (
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0')
        self.driver = webdriver.PhantomJS(executable_path=settings['PHANTOMJS'], desired_capabilities=self.dcap, )
        self.loginD(True)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        self.CurrentTime = time.time()
        if self.CurrentTime-self.startTime >= 3600 :
            self.loginD(self.change)
        self.driver.get(request.url)
        print("页面渲染中，请稍候等待····")
        print(self.driver.current_url)
        self.driver.implicitly_wait(10)
        print("保存图片：",self.driver.save_screenshot('screenshot\\weibo'+self.CurrentTime.__str__()+".png"))
        getMore = self.driver.find_elements_by_xpath('//div[@class="search_rese clearfix"]/a')
        if len(getMore) != 0: getMore[0].click();self.driver.implicitly_wait(10)
        comentMore = self.driver.find_elements_by_xpath('//a[@class="WB_text_opt"]')
        for item in comentMore:
            item.click()
            time.sleep(0.7)
        self.driver.implicitly_wait(5)
        if self.driver.current_url.find("Refer=g")!=-1:
            pageNum =self.driver.find_elements_by_xpath('//span[@class="list"]/a')
            logging.info(pageNum)
            if len(pageNum)!=0:pageNum[0].click()
            self.driver.implicitly_wait(5)
        rendered_body = self.driver.page_source
        self.driver.implicitly_wait(5)
        return HtmlResponse(request.url, body=rendered_body, encoding='utf-8')

    def login(self,change):
        self.startTime = time.time()
        logging.info("正在执行登陆操作，请稍候..............")
        self.dcap = dict(DesiredCapabilities.PHANTOMJS)
        self.dcap['phantomjs.page.setting.userAgent'] = (
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0')
        self.driver = webdriver.PhantomJS(executable_path=settings['PHANTOMJS'],desired_capabilities=self.dcap,)
        # self.driver = webdriver.PhantomJS(executable_path=settings['PHANTOMJS'])
        self.driver.set_window_size(1200, 600)
        self.driver.get("https://weibo.com")
        self.driver.implicitly_wait(10)
        # print("find element---------------" )
        if change :
            logging.info("切换账号准备中，切换为账号：--------------")
            logging.info(settings['USERNAME1'])
            self.change = False
            self.driver.find_element_by_xpath('//*[@id="loginname"]').send_keys(settings['USERNAME1'])
            self.driver.find_element_by_xpath('//*[@id="loginname"]').clear()
            self.driver.find_element_by_xpath('//*[@id="loginname"]').send_keys(settings['USERNAME1'])
            self.driver.find_element_by_xpath('//*[@type="password"]').send_keys(settings['PASSWD1'])
        else:
            logging.info("切换账号准备中，切换为账号：--------------")
            logging.info(settings['USERNAME2'])
            self.change = True
            self.driver.find_element_by_xpath('//*[@id="loginname"]').send_keys(settings['USERNAME2'])
            self.driver.find_element_by_xpath('//*[@id="loginname"]').clear()
            self.driver.find_element_by_xpath('//*[@id="loginname"]').send_keys(settings['USERNAME2'])
            self.driver.find_element_by_xpath('//*[@type="password"]').send_keys(settings['PASSWD2'])
        print("保存登录状况：",self.driver.save_screenshot("screenshot\\login.png"))
        self.driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()
        self.driver.implicitly_wait(10)
        print("保存登录后的状况：",self.driver.save_screenshot("screenshot\\logined.png"))
        print("登陆之后的页面为：" + self.driver.current_url)
    def logout(self):
        self.driver.quit()
        logging.info("休息三秒钟**********************")
        time.sleep(3)
    def loginD(self,change):
        self.startTime = time.time()
        logging.info("开始加载cookie信息，请稍候------")
        self.driver.get("https://weibo.com")
        self.driver.implicitly_wait(10)
        self.driver.delete_all_cookies()
        input=''
        if change:
            input='cookies\\14715399742'
            self.change=False
        else:
            input ='cookies\\13424333758'
            self.change=True
        print('加载cookie数据：',input)
        input = open(input,mode='rb')
        cookieList = pickle.load(input)
        input.close()
        for cookie in cookieList:
            # fix the problem-> "errorMessage":"Unable to set Cookie"
            for k in ('name', 'value', 'domain', 'path', 'expiry'):
                if k not in list(cookie.keys()):
                    if k == 'expiry':
                        t = time.time()
                        cookie[k] = int(t)  # 时间戳 秒
            self.driver.add_cookie({k: cookie[k] for k in ('name', 'value', 'domain', 'path', 'expiry') if k in cookie})
        self.driver.get("https://weibo.com")
        self.driver.implicitly_wait(10)
        logging.info(self.driver.current_url)
    def spider_closed(self, spider, reason):
        self.driver.close()
        second = time.time() -self.time
        spider.logger.info("本次爬取共花费时长(秒)：%s" % second)
        spider.logger.info("spider closed: %s" % spider.name)

    def spider_opened(self, spider):
        self.time = time.time()
        spider.logger.info('Spider opened: %s' % spider.name)

