#coding=utf-8

import os
S3LOG_CONFIG =      r"./s3files/s3log.config"

FILE_PATH_SBV =     r"./crawl_data/%s.csv"
FILE_PATH_VESSEL =  r"./crawl_data/%s.xml"
FILE_PATH_Port =    r"./crawl_data/%s_port.csv"

#是否scrapyd托管中
_managed_by_scrapyd = None
def managed_by_scrapyd():
    global _managed_by_scrapyd
    if _managed_by_scrapyd is None:
        _managed_by_scrapyd = os.environ.has_key("SCRAPY_FEED_URI")
    return _managed_by_scrapyd

SDATE_FORMAT = '%Y-%m-%d'  # 调用schedule.json时传递的SDATE格式