# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AgencyItem(scrapy.Item): #19
    # define the fields for your item here like:
    mode=scrapy.Field()
    agency_code = scrapy.Field()
    agency_name=scrapy.Field()
    agency_address=scrapy.Field()
    agency_contact_peple=scrapy.Field()
    agency_contact_phone=scrapy.Field()
    agency_certify=scrapy.Field()
    agency_gov=scrapy.Field()
    agency_doc=scrapy.Field()
    agency_starttime=scrapy.Field()
    agency_boss=scrapy.Field()
    agency_asset=scrapy.Field()
    agency_structrue=scrapy.Field()
    agency_accountor=scrapy.Field()
    agency_child=scrapy.Field()
    agency_partner=scrapy.Field()
    agency_cpa=scrapy.Field()
    agency_stuff=scrapy.Field()
    agency_totalcpa=scrapy.Field()
    agency_totalstuff=scrapy.Field()

class CpaItem(scrapy.Item): # 18
    mode=scrapy.Field()
    name=scrapy.Field()
    gender=scrapy.Field()
    birth=scrapy.Field()
    duty=scrapy.Field()
    party=scrapy.Field()
    education=scrapy.Field()
    degree=scrapy.Field()
    profession=scrapy.Field()
    school=scrapy.Field()
    method=scrapy.Field()
    exam_no=scrapy.Field()
    exam_year=scrapy.Field()
    certi_no=scrapy.Field()
    partner=scrapy.Field()
    certi_doc=scrapy.Field()
    certi_time=scrapy.Field()
    certi_agency=scrapy.Field()
    punish=scrapy.Field()
