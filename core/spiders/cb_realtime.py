#coding=utf-8
'''
抓取 CnBeta '实时更新'栏目的12个li.

Dom sample:
<li data-sid="336087">
    <div class="title">
        <a href="/articles/336087.htm" target="_blank">爱沙尼亚：欧盟五千亿欧元数字市场的模型</a>
    </div>
</li>
'''
from datetime import datetime as dt_cls

from scrapy.selector import Selector
from scrapy.http import Request, FormRequest

from s3_spider import S3Spider
from core.items import RealTimeMainItem

class CnBetaRealtime(S3Spider):
    name = 'cb_realtime'
    _pre_get_url = "http://www.cnbeta.com/"  #打开首页，获取Realtime列表

    def __init__(self, **kwargs):
        self._init_task(kwargs)

    def start_requests(self):
        result_list = [Request(url=CnBetaRealtime._pre_get_url,
                               callback=self._real_get)]
        return result_list

    def _real_get(self, response):
        hxs = Selector(response)
        realtime_li_list_xpath = "//div[@class='realtime_list']/ul/li"
        realtime_li_list = hxs.xpath(realtime_li_list_xpath)
        # realtime_li_list type: <class 'scrapy.selector.unified.SelectorList'>
        # realtime_li      type: <class 'scrapy.selector.unified.Selector'>
        
        #调用参数加入 SAVE_HTMLFILE=1 ， 用于保存临时页面用于查看
        self.save_htmlfile_if_assigned(str(response.body), "cb_realtime") 
        for realtime_li in realtime_li_list:
            
            sid_ulist = realtime_li.xpath("@data-sid").extract()  #sid unicode list
            sid_unicode= sid_ulist[0]
            sid = str(sid_unicode)
            
            item_main = RealTimeMainItem()
            item_main['Sid'] = sid
            
            link_tuple = self._get_link(realtime_li)
            item_main['Href'] = link_tuple[0]
            item_main['Title'] = link_tuple[1]
            yield item_main

    def _get_link(self, realtime_li):
        title_link = realtime_li.xpath("./div[@class='title']/a")[0]
        href_unicode = title_link.xpath("@href").extract()[0]
        title_unicode = title_link.xpath("./text()").extract()[0]
        return(str(href_unicode), str(title_unicode))