from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import  os
import tkinter
from  tkinter import *
from scrapy.http import HtmlResponse
import logging
import datetime
import time
import os
from urllib.request import quote

class spider:
    def __init__(self):
        settings = open('settings')
        self.weiboFile=settings.readline().split("=")[1].replace('\n','')
        self.personFile =settings.readline().split("=")[1].replace('\n','')
        self.chromeDriver =settings.readline().replace('\n','')
        self.profile_data =settings.readline().replace('\n','')
        self.initTool()
        self.loadWindow()
        pass

    def initTool(self):
        chromeDriver =self.chromeDriver
        profile_data=self.profile_data
        chrome_options=webdriver.ChromeOptions()
        chrome_options.add_argument("user-data-dir="+os.path.abspath(profile_data))
        os.environ["webdriver.chrome.driver"]=chromeDriver
        self.driver = webdriver.Chrome(executable_path=chromeDriver,port=0,chrome_options=chrome_options)
        self.driver.set_window_size(1500,800)
        # self.driver.get("http://s.weibo.com/weibo/kfc&c=spr_sinamkt_buy_hyww_weibo_t113&nodup=1")
        self.driver.implicitly_wait(30)
        # win = 'window.scrollTo(0,2200)'
        # self.driver.execute_script(script=win)
        # obj.execute_async_script(win)
    def loadWindow(self):
        top = tkinter.Tk()
        top.geometry("200x200")
        label = Label(top,text='状态信息：',bg='gray')
        # label.pack(side=LEFT)
        # label.grid(row=1, column=1, pady=5)
        Button(top, text="爬取微博数据", command=self.commandS).grid(row=2,column =2,pady =5)
        Button(top, text="爬取个人数据", command=self.loadPersonalPages).grid(row=3,column =2,pady =5)
        # 进入消息循环
        top.mainloop()

    def commandS(self):
        searchLink = open('searchLink')
        if os.path.exists(self.weiboFile):
            self.csv = open(self.weiboFile, mode='w+',encoding='utf-8')
        else:
            self.csv = open(self.weiboFile, mode='w+',encoding='utf-8')
            self.csv.write("昵称,微博内容,发博时间,终端,多媒体,发博地点,转发数,评论数,点赞数,主页网址\n")
        try:
            for link in searchLink.readlines():
                if link.strip()=='':continue
                # self.driver.get(quote(link))
                self.driver.get(link)
                self.pageProcess()
                response = HtmlResponse(self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
                self.exePageContent(response)
            self.csv.close()
        except Exception as e:
            print(e)
            self.csv.close()
            searchLink.close()
    def exePageContent(self, response):
        # logging.info("开始解析-------------")
        weiboContent = response.xpath('//div[@class="card-wrap" and @action-type="feed_list_item" and @mid]/div[@class="card"]')
        for weibo in weiboContent:
            name = weibo.xpath('.//a[@class="name"]/text()').extract()[0].replace("\\n|\\t| ", "").strip()
            print('获取微博信息开始，博主为：', name)
            detailUrl = weibo.xpath('.//a[@class="name"]/@href').extract()[0]
            article = weibo.xpath('.//p[@class="txt"][last()]').xpath('string(.)').extract()[0].replace("收起全文d","")
            # 获取发博定位地点
            # location = weibo.xpath('.//p[@class="from"]/p/a/span/em[last()]')
            # location = '' if len(location) == 0 else location.xpath('text()').extract()[0]
            location =""
            # article = article.replace("\u200b", "")
            # article = article.replace("\u261b", "")
            # article = article.replace("\xa5", "")
            # 获取是否有多媒体信息，图片视频等
            meidas = weibo.xpath('.//div[@class="media media-piclist"]')
            meidas = "有" if len(meidas) != 0 else "无"
            # 获取发布时间和发博客户端
            temp = weibo.xpath('.//p[@class="from"]/a')
            deployTime = temp[0].xpath('text()').extract()
            deploy = self.strTimeProcess('' if len(deployTime) == 0 else deployTime[0])
            client = "无" if len(temp) == 1 else temp[1].xpath('text()').extract()[0]
            # 获取
            comments = weibo.xpath('.//div[@class="card-act"]/ul/li')
            forward = comments[1].xpath('.//a/text()')[0].extract()
            comment = comments[2].xpath('.//a/text()')[0].extract()
            try:
                good = comments[3].xpath('.//a/em/text()')[0].extract()
            except:
                good=""
            # comment = comment.xpath('text()').extract() if len(comment) != 0 else 0
            # forward = forward.xpath('text()').extract() if len(forward) != 0 else 0
            # good = good.xpath('text()').extract() if len(good) != 0 else 0
            comment=comment.replace("评论","")
            forward=forward.replace("转发","")
            # print("------")
            if (type(forward) == list):
                forward = 0
            if (type(good) == list):
                good = 0
            if (type(comment) == list):
                comment = 0
            print('获取微博信息结束，博主为：',name)
            self.writeToFile(name,article,location,meidas,deploy,client,comment,forward,good,detailUrl)
        page = response.xpath('//a[@class="next"]/@href')
        if len(page) != 0:
            if "page=51" not in page[0].extract():
                self.nextPage()
        pass

    def strTimeProcess(self,strTime):
        '''
        格式化时间
        :param strTime: 时间字符串
        :return: 格式化之后的字符串
        '''
        if(strTime==""):
            d3 = datetime.datetime.now()
            deployTime = str(d3.year) + "年" + str(d3.month) + "月" + str(d3.day) + "日 " + str(d3.hour) + ":" + str(
                d3.minute)+"NO"
            return deployTime
        if( strTime.find("秒前")!=-1):
            d3 = datetime.datetime.now()
            deployTime = str(d3.year) + "年" + str(d3.month) + "月" + str(d3.day) + "日 " + str(d3.hour) + ":" + str(d3.minute)
            return deployTime
        if(strTime.find("分钟前")!=-1):
            d1 = datetime.datetime.now()
            d3 = d1 - datetime.timedelta(minutes=int(strTime[0:strTime.find("分钟前")]))
            # print(d3)
            deployTime = str(d3.year)+"年"+str(d3.month)+"月"+str(d3.day)+"日 "+str(d3.hour)+":"+str(d3.minute)
            return deployTime
        elif(strTime.find("今天")!=-1):
            d1 = datetime.datetime.now()
            ct= str(d1.year)+"年"+str(d1.month)+"月"+str(d1.day)+"日 "+strTime[(strTime.find("今天")+2):]
            return ct
        else:
            d1 = datetime.datetime.now()
            return str(d1.year)+"年"+strTime
    def writeToFile(self,name,article,location,media,deploy,client,comment,forward,good,detailUrl):
        self.csv.write(name.replace('\n',''))
        self.csv.write(",")
        self.csv.write(article.replace('\n',''))
        self.csv.write(",")
        self.csv.write(deploy)
        self.csv.write(",")
        self.csv.write(client)
        self.csv.write(",")
        self.csv.write(media)
        self.csv.write(",")
        self.csv.write(location)
        self.csv.write(",")
        self.csv.write(forward.__str__())
        self.csv.write(",")
        self.csv.write(comment.__str__())
        self.csv.write(",")
        self.csv.write(good.__str__())
        self.csv.write(",")
        self.csv.write("http:"+detailUrl)
        self.csv.write("\n")
        # print(name,article,location,media,deploy,client,comment,forward,good,detailUrl)
        pass
    def nextPage(self):
        '''
        进入下一页
        :return:
        '''
        next = self.driver.find_elements_by_xpath('//a[@class="next"]')
        # page = self.driver.find_elements_by_xpath('//a[@class="next"]')
        if len(next)!=0:
            time.sleep(5)
            next[0].click()
            self.pageProcess()
            response = HtmlResponse(self.driver.current_url, body=self.driver.page_source, encoding='utf-8')
            self.exePageContent(response)
        pass
    def pageProcess(self):
        '''
        处理页面的  查看全文按钮
        :return:
        '''
        comentMore = self.driver.find_elements_by_xpath('//a[@action-type="fl_unfold"]')
        for item in comentMore:
            item.click()
            time.sleep(0.7)

    #-------分界线-----读取个人信息的方法-----------------------------------
    def loadPersonInformation(self,response):
        baseInformation = response.xpath('//div[@class="PCD_text_b PCD_text_b2"]')
        # print(len(baseInformation))
        if len(baseInformation)==0:
            return
        FansAndFoucsNumEtc = response.xpath('//table[@class="tb_counter"]/tbody/tr/td/a/strong/text()').extract()
        auth = response.xpath('//div[@class="pf_photo"]/a[@class="icon_bed"]/em')
        auth = '' if len(auth)==0 else auth.xpath('@title').extract()[0]
        lv = response.xpath('//p[@class="level_info"]/span[1]/span/text()').extract()[0].replace("Lv.","")
        name = response.xpath('//ul[@class="clearfix"]/li[1]/span[2]/text()').extract()[0]
        creatLocation = response.xpath('//ul[@class="clearfix"]/li[2]/span[2]/text()').extract()[0]
        sex = response.xpath('//ul[@class="clearfix"]/li[3]/span[2]/text()').extract()[0]
        birthdayText = response.xpath('//ul[@class="clearfix"]/li[4]/span[1]/text()').extract()[0]
        birthday=''
        if birthdayText.strip().find("生日") != -1:
            birthday = response.xpath('//ul[@class="clearfix"]/li[4]/span[2]/text()').extract()[0]
        creatTime = response.xpath('//ul[@class="clearfix"]/li[last()]/span[2]').xpath('string(.)').extract()[0].strip()
        print("抓取个人信息，昵称为：",name)
        print("认证：",auth)
        self.writePersonInformation(name,auth,sex,FansAndFoucsNumEtc[0],FansAndFoucsNumEtc[1],FansAndFoucsNumEtc[2],
                                    lv,creatLocation,birthday,creatTime)
        pass
    def clickPersonPage(self):
        link = self.driver.find_elements_by_xpath('//div[@class="PCD_person_info"]/a')
        if len(link)!=0:
            time.sleep(3)
            link[0].click()
            self.driver.implicitly_wait(30)
            time.sleep(3)
            print(self.driver.current_url)
            self.driver.save_screenshot("information.png")
            response = HtmlResponse(self.driver.current_url,body=self.driver.page_source,encoding='utf-8')
            self.loadPersonInformation(response)
        pass
    def loadPersonalPages(self):
        links = open('personalLink',mode='r')
        linkReaded =open('personalLinkReaded',mode='w')
        if os.path.exists(self.personFile):
            self.personInformation = open(self.personFile,mode='w')
        else:
            self.personInformation = open(self.personFile,mode='w+')
            self.personInformation.write("昵称,认证,性别,关注数,粉丝数,微博数,等级,创建地点,生日,创建时间\n")
        try:
            for link in links.readlines():
                if link.strip() =='':continue
                self.driver.get(link)
                logging.info(link)
                self.clickPersonPage()
                linkReaded.write(link+"\n")
            self.personInformation.close()
        except :
            logging.error(link)
            linkReaded.close()
            links.close()
            self.personInformation.close()
    def writePersonInformation(self,name,auth,sex,focus,fans,articleNum,lv,createLocation,birthday,createTime):
        self.personInformation.write(name+",")
        self.personInformation.write(auth+",")
        self.personInformation.write(sex+",")
        self.personInformation.write(focus.__str__()+",")
        self.personInformation.write(fans.__str__()+",")
        self.personInformation.write(articleNum.__str__()+",")
        self.personInformation.write(lv.__str__()+",")
        self.personInformation.write(createLocation+",")
        self.personInformation.write(birthday+",")
        self.personInformation.write(createTime+"\n")
        pass
weiboSprider = spider()