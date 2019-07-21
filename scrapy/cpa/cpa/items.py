# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CpaItem(scrapy.Item):
    # define the fields for your item here like:
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
