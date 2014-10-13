#coding=utf-8
'''
***    BaseSpider for S3 spiders    ***

Tips for inherit spiders:
Have a consistent exception handling for 'parse',
but others like 'make_requests_from_url' should not.


'''

from scrapy.http import Request, FormRequest
from scrapy.exceptions import CloseSpider
from scrapy.spider import Spider
from scrapy.shell import inspect_response
from scrapy import log as scrapy_log


#from sss.page_info import PageInfo
import infrastructure.s3_util as s3_util


class S3Spider(Spider):
    #类成员用大写， name是特例，scrapy已定义
    name = 's3_spider(Base spider,custom spider should inherit from this class)'

    def _init_task(self, kwargs):
        '''
        从taskfile初始化任务
        '''
        self.pass_args = kwargs

    def stop(self, reason='manual stop'):
        msg = "Close spider %s cause: %s" % (self.name, reason)
        self.s3spider_log(msg, lv=scrapy_log.ERROR)
        raise CloseSpider(reason)

    def save_htmlfile_if_assigned(self, content, name):

        if self.pass_args.has_key("SAVE_HTMLFILE"):
            file_name = self.pass_args["SAVE_HTMLFILE"]
            file_path = 'crawl_data/%s/%s.html' % (self.name, file_name)
            try:
                file1 = open(file_path, 'a')
                file1.write(content)
                print 'Save html file successful.', file_path
            finally:
                file1.close()
        else:
            self.s3spider_log("Don't need to save html file.")

    def insp_response(self, response):
        inspect_response(response, self)

    @classmethod
    def raise_htmldom_notfound(cls, xpath):
        '''html 节点未找到的异常.'''
        import infrastructure.s3_exception
        raise infrastructure.s3_exception.DomNotFoundError(cls.name, xpath)

    def s3spider_log(self, message, lv = scrapy_log.INFO):
        msg = message+"[from s3_spider]"
        self.log(msg, lv)  #写到scrapyd目录
        if lv == scrapy_log.ERROR:
            s3_util.LogUtil.error(msg)  # 写到 s3files/s3logs/s3.log
        else:
            s3_util.LogUtil.info(msg)
        #todo 重构LogUtil，可以动态指定lv

