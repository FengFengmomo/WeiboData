# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class WeibodataPipeline(object):

    def open_spider(self, spider):
        '''
        打开文件
        :param spider:
        :return:
        '''
        self.csv = open('result/weibo.csv',mode='w+',encoding='utf-8')
        self.csv.write("昵称,微博内容,发博时间,终端,多媒体,发博地点,转发数,评论数,"
                       "点赞数,微博认证,微博等级,性别,微博创建时间,微创建地点,"
                       "关注数,粉丝数,微博数\n")

    def close_spider(self, spider):
        '''

        :param spider:
        :return:
        '''
        self.csv.close()

    def process_item(self, item, spider):
        if len(item.keys())<18:
            spider.logger.warn("该数据不符合要求！！！！！！！！！！！！！！！！！！！！！！！！")
            return item
        self.csv.write(item['name'])
        self.csv.write(",")
        self.csv.write(item['article'])
        self.csv.write(",")
        self.csv.write(item['date'])
        self.csv.write(",")
        self.csv.write(item['client'])
        self.csv.write(",")
        self.csv.write(item['media'])
        self.csv.write(",")
        self.csv.write(item['location'])
        self.csv.write(",")
        self.csv.write(item['forward'].__str__())
        self.csv.write(",")
        self.csv.write(item['comment'].__str__())
        self.csv.write(",")
        self.csv.write(item['good'].__str__())
        self.csv.write(",")
        self.csv.write(item['auth'])
        self.csv.write(",")
        self.csv.write(item['level'].__str__())
        self.csv.write(",")
        self.csv.write(item['sex'])
        self.csv.write(",")
        self.csv.write(item['creatTime'])
        self.csv.write(",")
        self.csv.write(item['creatLocation'])
        self.csv.write(",")
        self.csv.write(item['focusNum'].__str__())
        self.csv.write(",")
        self.csv.write(item['fansNum'].__str__())
        self.csv.write(",")
        self.csv.write(item['articleNum'].__str__())
        self.csv.write("\n")

        return item
