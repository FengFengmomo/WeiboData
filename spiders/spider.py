import scrapy
import logging
from urllib import parse
from WeiboData.items import WeibodataItem
import time
import datetime
from scrapy.conf import settings

class data(scrapy.Spider):
    name = 'loadData'
    allowed_domains =["weibo.com"]
    keyword = "kfc"
    # parse.urlencode()
    start_urls = [
        "http://s.weibo.com/weibo/"+keyword+"?topnav=1&wvr=6&b=1&c=spr_sinamkt_buy_hyww_weibo_t113"
    ]
    def __init__(self):
        self.processStartUrls()
        pass
        # 'http://s.weibo.com/weibo/kfc&typeall=1&suball=1&timescope=custom:2017-12-06-0:2017-12-06-23&Refer=g?c=spr_sinamkt_buy_hyww_weibo_p113'

    def parse(self, response):
        '''
        先获取本次获取得到的查询结果页面总共有多少页
        然后再依次在每页查询数据
        :param response:
        :return:
        '''
        pages =response.xpath('//span[@class="list"]//a')
        logging.info(pages)
        print("页面数量为：",len(pages))
        logging.info(len(pages))
        if len(pages)!=0 :
            for i in range(1,len(pages)-1):
                yield scrapy.Request(response.url+"&page="+str(i), callback=self.exePageContent)
        # print(response.url)
        # yield scrapy.Request(response.url+"&page=1", callback=self.exePageContent)
        else:
            yield scrapy.Request(response.url, callback=self.exePageContent)

    def exePageContent(self,response):
        logging.info("开始解析-------------")
        logging.info(response.url)
        weiboContent = response.xpath('//div[@class="feed_lists W_texta"]/div')
        for weibo in weiboContent:
            # weibo =weiboContent[0]
            logging.info("获取微博内容等信息开始----")
            self.item = WeibodataItem()
            name = weibo.xpath('.//a[@class="W_texta W_fb"]/text()').extract()[0].replace("\\n|\\t| ","").strip()
            detailUrl = weibo.xpath('.//a[@class="W_texta W_fb"]/@href').extract()[0]
            # print(name,": ",detailUrl)
            self.item['name'] = name
            # logging.info("取得姓名信息--------")
            article = weibo.xpath('.//p[@class="comment_txt"][last()]').xpath('string(.)').extract()[0].replace("收起全文d","").strip()
            #获取发博定位地点
            location = weibo.xpath('.//div[@class="feed_content wbcon"]/p/a/span/em[last()]')
            location = '' if len(location)==0 else location.xpath('text()').extract()[0]
            self.item['location'] =location
            self.item['article'] =article.replace("\u200b","")
            #获取是否有多媒体信息，图片视频等
            meidas =  weibo.xpath('.//div[@class="WB_media_wrap clearfix"]')
            self.item['media']= "有" if len(meidas)!=0 else "无"
            #获取发布时间和发博客户端
            temp = weibo.xpath('.//div[@class="feed_from W_textb"]/a')
            deployTime =temp[0].xpath('text()').extract()
            deploy = self.strTimeProcess('' if len(deployTime)==0 else deployTime[0])
            client ="无" if len(temp)==1 else temp[1].xpath('text()').extract()[0]
            self.item['date'] = deploy
            self.item['client'] = client
            #获取
            comments = weibo.xpath('.//div[@class="feed_action clearfix"]/ul/li')
            forward = comments[1].xpath('.//a/span/em')
            comment =comments[2].xpath('.//a/span/em')
            good =comments[3].xpath('.//a/span/em')
            self.item['comment'] = comment.xpath('text()').extract() if len(comment)!=0 else 0
            self.item['forward'] = forward.xpath('text()').extract() if len(forward)!=0 else 0
            self.item['good'] = good.xpath('text()').extract() if len(good)!=0 else 0
            # print("------")
            if (type(self.item['forward'])==list):
                self.item['forward'] = 0
            if (type(self.item['good'])==list):
                self.item['good'] = 0
            if (type(self.item['comment'])==list):
                self.item['comment'] = 0
            logging.info("获取微博内容等信息结束----")
            yield scrapy.Request(url="https:"+detailUrl,meta={'item':self.item}, callback=self.searchUserDataMidder)
            pass
    def searchUserDataMidder(self,response):
        Citem = response.meta['item']
        logging.info("开始获取认证信息与粉丝数关注数等信息：")
        authAndLv = response.xpath('//div[@class="verify_area W_tog_hover S_line2"]')
        if len(authAndLv)==0:
            Citem['auth'] = '否'
        else:
            Citem['auth'] = '是'
        try:
            FansAndFoucsNumEtc = response.xpath('//table[@class="tb_counter"]/tbody/tr/td/a/strong/text()').extract()
            print("粉丝信息长度为：",len(FansAndFoucsNumEtc))
            if len(FansAndFoucsNumEtc)==0:
                FansAndFoucsNumEtc = response.xpath('//td[@class="S_line1"]/strong/text()').extract()
                print("重新获取粉丝信息：",FansAndFoucsNumEtc)
            Citem['focusNum'] = FansAndFoucsNumEtc[0]
            Citem['fansNum'] = FansAndFoucsNumEtc[1]
            Citem['articleNum'] = FansAndFoucsNumEtc[2]
        except:
            logging.info("抓取粉丝数关注数信息错误**********************")
            # logging.WARN(FansAndFoucsNumEtc)
            Citem['focusNum'] = '无'
            Citem['fansNum'] = '无'
            Citem['articleNum'] = '无'
            pass

        try:
            detailUrl = response.xpath('//div[@class="PCD_person_info"]/a/@href').extract()
            logging.info(detailUrl)
            detailUrl = detailUrl[0] if len(detailUrl)!=0 else detailUrl
        except:
            logging.warning("error-----------------")
            logging.info("重新获取粉丝和关注信息---------")
            yield scrapy.Request(url=response.url, meta={'item': Citem},
                                 callback=self.searchUserDataMidder)
        # logging.info(detailUrl)
        logging.info("获取认证信息结束---------")
        yield scrapy.Request(url="https://weibo.com"+detailUrl,meta={'item':Citem}, callback=self.searchUserData)
        pass
    def searchUserData(self,response):
        Citem = response.meta['item']
        # try:
        logging.info("开始获取个人信息：")
        lv = response.xpath('//p[@class="level_info"]/span[1]/span/text()').extract()
        if type(lv) == list and len(lv)==1:
            lv = lv[0]
        logging.info("等级信息为：----------")
        logging.info(lv)
        try:
            Citem['level'] = lv.replace("Lv.","")
        except:
            Citem['level'] = lv[0].replace("Lv.","")
        try:
            creatLocation = response.xpath('//ul[@class="clearfix"]/li[2]/span[2]/text()').extract()[0]
            sex = response.xpath('//ul[@class="clearfix"]/li[3]/span[2]/text()').extract()[0]
            birthdayText = response.xpath('//ul[@class="clearfix"]/li[4]/span[1]/text()').extract()[0]
            if birthdayText.strip() =="生日":
                birthday = response.xpath('//ul[@class="clearfix"]/li[4]/span[2]/text()').extract()[0]
                Citem['birthday'] = birthday
            else:
                Citem['birthday'] = ''
            creatTime = response.xpath('//ul[@class="clearfix"]/li[last()]/span[2]').xpath('string(.)').extract()[0].strip()
            cc = response.xpath('//ul[@class="clearfix"]/li[last()]/span[1]')
            Citem['creatLocation'] = creatLocation
            Citem['creatTime'] =creatTime
            Citem['sex'] = sex
            logging.info("获取个人信息结束：")
        except IndexError as e:
            Citem['creatLocation'] = ""
            Citem['creatTime'] = ""
            Citem['sex'] = ""
            logging.info("该用户为非个人微博")
        # logging.info("未获得该用户的个人信息")
        yield Citem


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
    def processStartUrls(self):
        startTime = settings['STARTTIME']
        endTime = settings['ENDTIME']
        step = settings['STEP']
        d1 = datetime.datetime(int(startTime[0:4]), int(startTime[5:7]), int(startTime[8:10]))
        d2 = datetime.datetime(int(endTime[0:4]), int(endTime[5:7]), int(endTime[8:10]))
        change = False
        self.start_urls.clear()
        if (d2 - d1).days == 0:
            url = 'http://s.weibo.com/weibo/kfc&typeall=1&suball=1&timescope=custom:'+d1.__str__()[0:10]+'-0:'+d2.__str__()[0:10]+'-23&Refer=g?c=spr_sinamkt_buy_hyww_weibo_p113&page=1'
            self.start_urls.append(url)
            logging.info(self.start_urls)
            logging.info("初始化开始链接完毕")
            logging.info("开始准备进行登陆操作")
            return
        while ((d2 - d1).days >= 1):
            if (d2 - d1).days >= 10:
                temp = d1 + datetime.timedelta(days=step)
            else:
                temp = d2
            if change:
                d1 = d1 + datetime.timedelta(days=1)
            change = True
            url = 'http://s.weibo.com/weibo/byd&typeall=1&suball=1&timescope=custom:'+d1.__str__()[0:10]+'-0:'+temp.__str__()[0:10]+'-23&Refer=g?c=spr_sinamkt_buy_hyww_weibo_p113&page=1'
            self.start_urls.append(url)
            # print(d1, temp)
            d1 = temp
        logging.info(self.start_urls)
        logging.info("初始化开始链接完毕")
        logging.info("开始准备进行登陆操作")
# strTimeProcess("11分钟前")
# strTimeProcess("今天00:09")
# strTimeProcess("12月23日18:01")