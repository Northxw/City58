# -*- coding: utf-8 -*-

import random

# CRAWLER NAME
BOT_NAME = 'City58'

SPIDER_MODULES = ['City58.spiders']
NEWSPIDER_MODULE = 'City58.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 100

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = eval('%.1f'%random.random())

# 下载超时时间
DOWNLOAD_TIMEOUT = 10

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'City58.middlewares.City58SpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'City58.middlewares.RandomUAMiddleware': 490,
    'City58.middlewares.ProxyMiddleware': 500,
    'City58.middlewares.DownloadRetryMiddleware': 510
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'City58.pipelines.MysqlTwistedPipeline': 300,
    # 'City58.pipelines.JsonPipeline': 301,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
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

# City
HOST = 'xa.58.com'

# Xdaili_Proxy
XDL_ORDERNO = 'Yw1234567891022oXkjo'
XDL_SECRET = 'bdfdhdkalsca5cdva5va1vsdv9ac7e7'
XDL_IP = "forward.xdaili.cn"
XDL_PORT = '80'

# Abuyun_Proxy
PROXY_SERVER = "http://http-dyn.abuyun.com:9020"
PROXY_USER = "H5X326C55VQR52ED"
PROXY_PASS = "51BF412660000891"

# MYSQL SEETINGS
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_DB = 'city58'
MYSQL_PORT = 3306

# EMAIL SETTINGS
MAIL_FROM = 'northxw@163.com'
MAIL_HOST = 'smtp.163.com'
MAIL_PORT = 25
MAIL_USER = 'northxw@163.com'
MAIL_PASS = 'authcode'
RECEIVE_LIST = ['northxw@qq.com', 'northxw@sina.com']
SUBJECT = 'Crawler Status Report'