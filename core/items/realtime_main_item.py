#coding=utf-8
from scrapy.item import Item, Field

#sample 页面:http://www.cnbeta.com/articles/336025.htm

class RealTimeMainItem(Item):
    Sid = Field()  # 336025
    Title = Field()  # 美为阿富汗购5亿美元军机 变废品每磅6美分卖出（抓取原始值为unicode编码，需要转码）

