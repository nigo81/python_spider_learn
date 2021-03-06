# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from cpa.items import AgencyItem
from cpa.items import CpaItem
class CpaPipeline(object):
    def open_spider(self,spider):
        # self.csv_file = open("agency.csv",'w',encoding='GB18030',newline='')
        # # 定义一个列表，用于整合所有的信息
        # self.csv_items = []

        #处理人员信息
        self.csv_file_peple=open("cpa.csv","w",encoding="GB18030",newline='')
        self.csv_people=[]
    def process_item(self, item, spider):
        # 定义一个item用于整合每一个item的信息

        # if item["mode"]=="agency":
        #     item_csv = []
        #     item_csv.append(item["agency_code"])
        #     item_csv.append(item["agency_name"])
        #     item_csv.append(item["agency_address"])
        #     item_csv.append(item["agency_contact_peple"])
        #     item_csv.append(item["agency_contact_phone"])
        #     item_csv.append(item["agency_certify"])
        #     item_csv.append(item["agency_gov"])
        #     item_csv.append(item["agency_doc"])
        #     item_csv.append(item["agency_starttime"])
        #     item_csv.append(item["agency_boss"])
        #     item_csv.append(item["agency_asset"])
        #     item_csv.append(item["agency_structrue"])
        #     item_csv.append(item["agency_accountor"])
        #     item_csv.append(item["agency_child"])
        #     item_csv.append(item["agency_partner"])
        #     item_csv.append(item["agency_cpa"])
        #     item_csv.append(item["agency_stuff"])
        #     item_csv.append(item["agency_totalcpa"])
        #     item_csv.append(item["agency_totalstuff"])
        #     self.csv_items.append(item_csv)
        #elif item["mode"]=="people":
        csv_people=[]
        csv_people.append(item["name"])
        csv_people.append(item["gender"])
        # try:
        #     csv_people.append(item["birth"])
        # except:
        #     pass
        csv_people.append(item["duty"])
        csv_people.append(item["party"])
        csv_people.append(item["education"])
        csv_people.append(item["degree"])
        csv_people.append(item["profession"])
        csv_people.append(item["school"])
        csv_people.append(item["method"])
        csv_people.append(item["exam_no"])
        csv_people.append(item["exam_year"])
        csv_people.append(item["certi_no"])
        csv_people.append(item["partner"])
        csv_people.append(item["certi_doc"])
        csv_people.append(item["certi_time"])
        csv_people.append(item["certi_agency"])
        csv_people.append(item["punish"])
        self.csv_people.append(csv_people)

    def close_spider(self,spider):
        # 处理机构信息
        # writer = csv.writer(self.csv_file)
        # writer.writerow(["agency_code","agency_name","agency_address","agency_contact_peple","agency_phone",
        # "agency_certify","agency_gov","agency_doc","agency_starttime","agency_boss","agency_asset",
        # "agency_structrue","agency_accountor","agency_child","agency_partner","agency_cpa",
        # "agency_stuff","agency_totalcpa","agency_totalstuff"])
        # writer.writerows(self.csv_items)
        # self.csv_file.close()

        #处理人员信息
        writer_people=csv.writer(self.csv_file_peple)
        writer_people.writerow(["name","gender","duty","party","education","degree","profession",
        "school","method","exam_no","exam_year","certi_no","partner","certi_doc","certi_time",
        "certi_agency","punish"])
        writer_people.writerows(self.csv_people)
        self.csv_file_peple.close()
        
        #return item
