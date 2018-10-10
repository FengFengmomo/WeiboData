# -*- coding: utf-8 -*-

# Scrapy settings for WeiboData project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'WeiboData'

SPIDER_MODULES = ['WeiboData.spiders']
NEWSPIDER_MODULE = 'WeiboData.spiders'

USERNAME4 = '15639914279'
PASSWD4 = 'qq125680'
USERNAME3 = '1026198058@qq.com'
PASSWD3 = 'T1026198058'
USERNAME2 = '14715399742'
PASSWD2 = 'z123456'
USERNAME1 = '18240701339'
PASSWD1 = '971111wumengying'
#http://www.xiaohao.kim/daili.php/index/index  user:qq125680 pwd:qq125680
UserAgent =['14715399742-z123456','13424333758----yx123456 ']
STARTTIME = '2017-12-25'
ENDTIME = '2017-12-26'
STEP = 1
#step 为搜索时间间隔,0表示为不采用时间间隔
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'WeiboData (+http://www.fiberhome.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True
ROBOTSTXT_OBEY = False

#禁止http重试下载
RETRY_ENABLED = False
#禁止重定向，防止request数量异常
REDIRECT_ENABLED = False
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

#seconds
DOWNLOAD_DELAY = 0.25

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

#设置日志级别
LOG_LEVEL = 'INFO'

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#   'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'WeiboData.middlewares.WeibodataSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
PHANTOMJS="E:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe"


DOWNLOADER_MIDDLEWARES = {
# 'WeiboData.middlewares.MyCustomDownloaderMiddleware': 543,
# 'WeiboData.middlewares.WeibodataSpiderMiddleware': None,
#     'WeiboData.middlewares.JsProcessWithoutLogin': 543,
    'WeiboData.middlewares.JsAjaxHtml': 600,

}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'WeiboData.pipelines.WeibodataPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#a custom cache storage backend:
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
