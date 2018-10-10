# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeibodataItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    article = scrapy.Field() #微博内容
    date = scrapy.Field()   #发博时间
    client = scrapy.Field() #发博文的终端
    media = scrapy.Field()  #多媒体,有、无
    location = scrapy.Field() #发博地点
    forward = scrapy.Field() #转发数
    comment = scrapy.Field() #评论数
    good = scrapy.Field()   #点赞数

    auth = scrapy.Field() # 是否微博认证
    level = scrapy.Field() #微博等级
    sex = scrapy.Field() #性别
    birthday =scrapy.Field() #生日
    creatTime = scrapy.Field() #微博创建时间
    creatLocation = scrapy.Field() #微创建地点
    focusNum  = scrapy.Field() #关注数
    fansNum =scrapy.Field() #粉丝数
    articleNum =scrapy.Field() #微博数
