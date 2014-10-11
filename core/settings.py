#coding=utf-8

# Scrapy settings for sss project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

#Scrapy 设置
BOT_NAME = 'spider_man'

#LOG_FILE = "./sss/files/log_global.txt"

SPIDER_MODULES = ['core.spiders']
NEWSPIDER_MODULE = 'core.spiders'


S3EXT_ENABLED = True
COOKIES_DEBUG = False
DOWNLOAD_DELAY = 2 #马斯基若不限制，会有部分request失败

#此配置影响scrapyd的输出格式
FEED_FORMAT = 'json'  #可用默认，若用自定义，在FEED_EXPORTERS取名字

#3.wingide测试时存储位置   Storages: file,s3,ftp,stdout，有scrapyd的item，就不用此配置
FEED_URI = 'file:./core/crawl_data/%(name)s/item%(time)s.json'

