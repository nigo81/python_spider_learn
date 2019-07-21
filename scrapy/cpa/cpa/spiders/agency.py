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
        for i in range(2,int(total_pages)+1):#int(total_pages)+1
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
            print(item)
            yield item
        # total_pages=response.xpath('//div[@id="pageCtr_basePageDiv"]/a[2]/@href').extract_first()      
        # total_pages=re.search("(\d+)",total_pages).group(1)
        # next_url='http://cmispub.cicpa.org.cn/cicpa2_web/OfficeIndexAction.do'
        # for i in range(2,3):#int(total_pages)+1
        #     data={
        #         'pageSize':'15',
        #         'pageNum':str(i),
        #         'method':'indexQuery',
        #         'queryType':'1',
        #         'isStock':'00',
        #         'ascGuid':'00'
        #     }
 #           print("当前页数" + str(i) + "总页数" +total_pages)
                    
#            yield scrapy.FormRequest(next_url,formdata=data,callback=self.parse_post,dont_filter=True)

