#coding=utf-8
from datetime import datetime as dt_cls

from scrapy.selector import Selector
from scrapy.http import Request, FormRequest

from s3_spider import S3Spider

#from sss.items.sbp_item import SBPItem, DockItem
from core.items.realtime_main_item import RealTimeMainItem

#_TIME_FORMAT = '%d-%b-%Y %H:%M'

class CnBetaRealtime(S3Spider):
    name = 'cb_realtime'
    _pre_get_url = "http://www.cnbeta.com/"

    def __init__(self, **kwargs):
        self._init_task(kwargs)

    def start_requests(self):
        result_list = [Request(url=CnBetaRealtime._pre_get_url,
                               callback=self._real_get)]
        return result_list

    def _real_get(self, response):
        self.save_htmlfile_if_assigned(str(response.body), "cb_realtime")
        hxs = Selector(response)
        
        list_xpath = "//div[@class='realtime_list']/ul/li"
        realtime_list = hxs.xpath(list_xpath)
        for realtime_main in realtime_list:
            self.insp_response(response)
            url_info = realtime_main.xpath("/div[@class='title']/a")
            print url_info
        
    #def _prepare_arguments(self):
        #start_date = dt_cls.strptime(self.pass_args['SDATE'], SDATE_FORMAT)
        #self.pass_args['P0'] = start_date.strftime('%d').lstrip('0')
        #self.pass_args['P1'] = start_date.strftime('%m').lstrip('0')
        #self.pass_args['P2'] = start_date.strftime('%Y').lstrip('0')

    ## class 为 schedulesFirstItemHeader 的父节点table才是结果所在table
    #def parse(self, response):
        #self.save_htmlfile_if_assigned(str(response.body), "msk")
        #hxs = Selector(response)
        #xpath_tables = "//table[@class='lstBox' and .//td[@class='schedulesFirstItemHeader']]"
        #schedule_tables = hxs.xpath(xpath_tables)

        #for tb in schedule_tables:  #一个tab，一个SBPItem，N个DockItem
            #docks = []
            #data_rows = tb.xpath(".//tr[contains(@class, 'Row')]")
            #for row in data_rows:
                #datas = row.xpath("./td")
                #dock1 = DockItem()

                #location_list = datas[1].xpath("./text()").extract()
                #if len(location_list) > 0:
                    #dock1['Location'] = clear_text(location_list[0])

                #vesselname_list = datas[4].xpath("./text()").extract()
                #if len(vesselname_list) > 0:
                    #dock1['VesselName'] = clear_text(vesselname_list[0])

                #eta_list = datas[2].xpath("./text()").extract()
                #if len(eta_list) > 0:
                    #dock1['Arrival'] = _msk_parse_time(eta_list[0])
                    ##eta_list[0]为&nbsp;(空格被html_encode 编码后)
                    ##u"Â "(空格的unicode，在watch窗口以外的地方，显示 \xa0)
                    ##\xc2\xa0(encode('utf-8'))

                #etd_list = datas[3].xpath("./text()").extract()
                #if len(etd_list) > 0:
                    #dock1['Departure'] = _msk_parse_time(etd_list[0])

                #voyageno_list = datas[5].xpath("./text()").extract()
                #if len(voyageno_list) > 0:
                    #dock1['VoyageNo'] = clear_text(voyageno_list[0])

                #docks.append(dock1)

            #xpath_transmit_time = ".//td[@class='schedulesFirstItemHeader']/text()"
            #transmit_time = clear_text(tb.xpath(xpath_transmit_time)[0].extract())
            #sbp1 = SBPItem()
            #sbp1['Carrier'] = self.SHIP_OWNER
            #sbp1['TransmitTime'] = pickup_number(transmit_time)
            #sbp1['PortOfLoading'] = docks[0]['Location']
            #sbp1['ETD'] = docks[0]['Departure']
            #sbp1['PortOfDischarge'] = docks[len(docks) - 1]['Location']
            #sbp1['ETA'] = docks[len(docks) - 1]['Arrival']
            #sbp1['Docks'] = docks
            #yield sbp1

#def _msk_parse_time(time_unicode):
    #if time_unicode == u"\xa0":  #首班没有arrival time， 末班没有departure time
        #return None
    #time_str_clean = clear_text(time_unicode)
    #return parse_time(time_str_clean, _TIME_FORMAT)