# -*- coding: utf-8 -*-
import scrapy
from cpa.items import AgencyItem
from cpa.items import CpaItem
import re
import json
from lxml import etree
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
        print("nigo:total pages" +str( int(total_pages)+1))
        for i in range(1,2): #int(total_pages)+1
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
        item=AgencyItem()
        for tr in trs:
            item['mode']="agency"
            item['agency_code']=tr.xpath('./td/text()').extract()[1]
            item['agency_name']=tr.xpath('./td/a/text()').extract_first()
            item['agency_address']=tr.xpath('./td/text()').extract()[2]
            item['agency_contact_peple']=tr.xpath('./td/text()').extract()[3]
            item['agency_contact_phone']=tr.xpath('./td/text()').extract()[4]
            #print(item)
            # 获取机构详细页的ID链接
            info=tr.xpath('./td/a/@href').extract_first()

            page_id=re.search("'(\w+)','(\d+)'",info).group(1)
            url='http://cmispub.cicpa.org.cn/cicpa2_web/09/' + page_id +'.shtml'
            yield scrapy.Request(url,callback=self.parse_agency,meta=item,dont_filter=True)
            
            #处理人员信息
            data={
                'method':'getPersons',
                'offGuid':page_id,
                'pageNum':'1',
                'pageSize':'10'
            }
            headers={
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko Core/1.70.3676.400 QQBrowser/10.4.3505.400'
            }                       
            peple_list_url='http://cmispub.cicpa.org.cn/cicpa2_web/OfficeIndexAction.do'
            yield scrapy.FormRequest(peple_list_url,formdata=data,headers=headers,callback=self.peoplelist,dont_filter=True)

    def parse_agency(self, response):
        item=response.meta
        item['agency_certify']=response.xpath('//*[@id="detailtb"]/tr[3]/td[4]/text()').extract_first().strip()
        item['agency_gov']=response.xpath('//*[@id="detailtb"]/tr[9]/td[2]/text()').extract_first().strip()
        item['agency_doc']=response.xpath('//*[@id="detailtb"]/tr[9]/td[4]/text()').extract_first().strip()
        item['agency_starttime']=response.xpath('//*[@id="detailtb"][1]/tr[9]/td[6]/text()').extract_first().strip()
        item['agency_boss']=response.xpath('//*[@id="detailtb"]/tr[10]/td[2]/text()').extract_first().strip()
        item['agency_asset']=response.xpath('//*[@id="detailtb"]/tr[10]/td[4]/text()').extract_first().strip()
        item['agency_structrue']=response.xpath('//*[@id="detailtb"]/tr[10]/td[6]/text()').extract_first().strip()
        item['agency_accountor']=response.xpath('//*[@id="detailtb"]/tr[11]/td[2]/text()').extract_first().strip()
        child=response.xpath('//*[@id="detailtb"]/tr[12]/td[2]/text()').extract_first()
        try:
            item['agency_child']=child.split("（详见设立分所情况）",1)[0].strip()
        except:
            item['agency_child']=0
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
        #print(item)
        yield item

    # 处理注册会计师列表页 暂未考虑翻页
    def peoplelist(self,response):
        details=response.xpath("//table[@id='pertable']//td/a/@onclick").extract()
        for detail in details:
            pid=re.search("'(\w+)','",detail).group(1)
            peple_content_url='http://cmispub.cicpa.org.cn/cicpa2_web/07/'+ pid + '.shtml'
            yield scrapy.Request(peple_content_url,callback=self.peoplecontent,dont_filter=True)
    def peoplecontent(self,response):
        item=CpaItem()
        item["mode"]="people"
        item["name"]=response.xpath('//table[@id="detailtb"]/tr[3]/td[2]/text()').extract_first().strip()
        item["gender"]=response.xpath('//table[@id="detailtb"]/tr[3]/td[4]/text()').extract_first().strip()
        # try:
        #     print(response.text)
        #     pattern="出生日期\s*</td>\s*<td class=.data_tb_content.\s*width='12%'>\s*(\d{4}-\d{2}-\d{2})"
        #     birth_text=re.search("pattern",response.text).group(1)
        #     print(birth_text)
        #     item["birth"]=birth_text
        # except:
        #     pass
        item["duty"]=response.xpath('//table[@id="detailtb"]/tr[3]/td[6]/text()').extract_first().strip()
        item["party"]=response.xpath('//table[@id="detailtb"]/tr[3]/td[8]/text()').extract_first().strip()
        item["education"]=response.xpath('//table[@id="detailtb"]/tr[5]/td[2]/text()').extract_first().strip()
        item["degree"]=response.xpath('//table[@id="detailtb"]/tr[5]/td[4]/text()').extract_first().strip()
        item["profession"]=response.xpath('//table[@id="detailtb"]/tr[5]/td[6]/text()').extract_first().strip()
        item["school"]=response.xpath('//table[@id="detailtb"]/tr[5]/td[8]/text()').extract_first().strip()
        item["method"]=response.xpath('//table[@id="detailtb"]/tr[7]/td[2]/text()').extract_first().strip()
        item["exam_no"]=response.xpath('//table[@id="detailtb"]/tr[9]/td[2]/text()').extract_first().strip()
        item["exam_year"]=response.xpath('//table[@id="detailtb"]/tr[9]/td[4]/text()').extract_first().strip()
        item["certi_no"]=response.xpath('//table[@id="detailtb"]/tr[11]/td[2]/text()').extract_first().strip()
        item["partner"]=response.xpath('//table[@id="detailtb"]/tr[11]/td[4]/text()').extract_first().strip()
        item["certi_doc"]=response.xpath('//table[@id="detailtb"]/tr[12]/td[2]/text()').extract_first().strip()
        item["certi_time"]=response.xpath('//table[@id="detailtb"]/tr[12]/td[4]/text()').extract_first().strip()
        item["certi_agency"]=response.xpath('//table[@id="detailtb"]/tr[13]/td[2]/text()').extract_first().strip()
        item["punish"]=response.xpath('//table[@id="detailtb"]/tr[16]/td[2]/text()').extract_first().strip()
        print(item)
        yield item

            

