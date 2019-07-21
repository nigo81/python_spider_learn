# -*- coding: utf-8 -*-
import scrapy
from cpa.items import CpaItem
import re
import json
class AgencySpider(scrapy.Spider):
    name = 'agency'
    allowed_domains = ['cmispub.cicpa.org']
    start_urls = ['http://cmispub.cicpa.org.cn/cicpa2_web/OfficeIndexAction.do']


    def start_requests(self):
        headers={
            'Referer':'http://cmispub.cicpa.org.cn/cicpa2_web/public/query2/1/00.shtml',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko Core/1.70.3676.400 QQBrowser/10.4.3505.400'
        }
        data={
            'pageSize':'15',
            'pageNum':'1',
            'method':'indexQuery',
            'queryType':'1',
            'isStock':'00',
            'ascGuid':'00'
        }
        request=scrapy.FormRequest('http://cmispub.cicpa.org.cn/cicpa2_web/OfficeIndexAction.do',
                        callback=self.parse_pages,
                        formdata=data,
                        headers=headers)
        yield request
    def parse(self, response):
        pass
    def parse_pages(self,response):
        total_pages=response.xpath('//div[@id="pageCtr_basePageDiv"]/a[2]/@href').extract_first()      
        total_pages=re.search("(\d+)",total_pages).group(1)
        headers={
            'Referer':'http://cmispub.cicpa.org.cn/cicpa2_web/public/query2/1/00.shtml',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko Core/1.70.3676.400 QQBrowser/10.4.3505.400'
        }
        for i in range(2,3):#int(total_pages)+1
            data={
                'pageSize':'15',
                'pageNum':str(i),
                'method':'indexQuery',
                'queryType':'1',
                'isStock':'00',
                'ascGuid':'00'
            }
            request=scrapy.FormRequest('http://cmispub.cicpa.org.cn/cicpa2_web/OfficeIndexAction.do',
                            callback=self.parse_post,
                            formdata=data,
                            headers=headers,
                            dont_filter=True)
            yield request        
    def parse_post(self,response):
        trs=response.xpath("//tr[@class='rsTr']")
        item=CpaItem()
        for tr in trs:
            item['agency_code']=tr.xpath('./td/text()').extract()[1]
            item['agency_name']=tr.xpath('./td/a/text()').extract_first()
            item['agency_address']=tr.xpath('./td/text()').extract()[2]
            item['agency_contact_peple']=tr.xpath('./td/text()').extract()[3]
            item['agency_contact_phone']=tr.xpath('./td/text()').extract()[4]
            #print(item)

            info=tr.xpath('./td/a/@href').extract_first()
            print(info)

            page_id=re.search("'(\w+)','(\d+)'",info).group(1)
            print(page_id)
            url='http://cmispub.cicpa.org.cn/cicpa2_web/09/' + page_id +'.shtml'
            yield scrapy.Request(url,callback=self.parse_agency,meta=item,dont_filter=True)
            #yield item
    def parse_agency(self, response):
        print("nigo:parse")
        item=response.meta
        item['agency_certify']=response.xpath('//*[@id="detailtb"]/tr[3]/td[4]/text()').extract_first().strip()
        item['agency_gov']=response.xpath('//*[@id="detailtb"]/tr[9]/td[2]/text()').extract_first().strip()
        item['agency_doc']=response.xpath('//*[@id="detailtb"]/tr[9]/td[4]/text()').extract_first().strip()
        item['agency_starttime']=response.xpath('//*[@id="detailtb"][1]/tr[9]/td[6]/text()').extract_first().strip()
        item['agency_boss']=response.xpath('//*[@id="detailtb"]/tr[10]/td[2]/text()').extract_first().strip()
        item['agency_asset']=response.xpath('//*[@id="detailtb"]/tr[10]/td[4]/text()').extract_first().strip()
        item['agency_structrue']=response.xpath('//*[@id="detailtb"]/tr[10]/td[6]/text()').extract_first().strip()
        item['agency_accountor']=response.xpath('//*[@id="detailtb"]/tr[11]/td[2]/text()').extract_first().strip()
        item['agency_child']=response.xpath('//*[@id="detailtb"]/tr[12]/td[2]/text()').extract_first().strip()
        partner=response.xpath('//*[@id="detailtb"]/tr[12]/td[4]/a/text()').extract_first()
        try:
            item['agency_partner']=partner.split("（请点击）",1)[0].strip()
        except  AttributeError:
            item['agency_partner']=0
        cpa=response.xpath('//*[@id="detailtb"]/tr[13]/td[2]/a/text()').extract_first()
        try:
            item['agency_cpa']=cpa.split("（请点击）",1)[0].strip()
        except AttributeError:
            item['agency_cpa']=0
        stuff=response.xpath('//*[@id="detailtb"]/tr[13]/td[4]/a/text()').extract_first()
        try:
            item['agency_stuff']=stuff.split("（请点击）",1)[0].strip()
        except AttributeError:
            item['agency_stuff']=0
        item['agency_totalcpa']=response.xpath('//*[@id="detailtb"]/tr[14]/td[2]/text()').extract_first().strip()
        item['agency_totalstuff']=response.xpath('//*[@id="detailtb"]/tr[14]/td[4]/text()').extract_first().strip()
        print(item)
        yield item

