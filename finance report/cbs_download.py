import requests
from lxml import etree
import re
import pandas as pd
class Login(object):
    def __init__(self):
        self.headers={
            'Referer':'https://caibaoshuo.com/',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
            'Content-Type':'application/x-www-form-urlencoded'
        }

        self.session=requests.Session()
        self.signin_url='https://caibaoshuo.com/ajax_signin_or_signup'
        self.code_url='https://caibaoshuo.com/verification_codes'
        self.signed_url='https://caibaoshuo.com/account/level'
        self.profit=[]
        self.profit_data=[]
        self.net_profit=[]
        self.net_profit_data=[]
        self.turnover=[]
        self.turnover_data=[]
        self.inventory=[]
        self.inventory_data=[]
        self.receivable=[]
        self.receivable_data=[]
        self.level=[]
        self.level_data=[]
        self.quick=[]
        self.quick_data=[]
        self.interest=[]
        self.interest_data=[]
        self.cash_ratio=[]
        self.cash_ratio_data=[]
        self.cash=[]
        self.cash_data=[]
    def login(self,phone):
        data={
            'utf8':'✓',
            'users_phone_signin_or_signup[phone_number]':phone,
            'users_phone_signin_or_signup[otp]':self.code(phone),
            'commit':'登录'
        }
        response=self.session.post(self.signin_url,data=data,headers=self.headers)
        if response.status_code==200:
            print("登录成功")
        else:
            print("登录失败")
    def code(self,phone):
        data={

            'phone_number':phone,
            'category':'signin_or_signup'
        }
        self.session.post(self.code_url,data=data)
        name=input("请输入验证码")
        return name
    # def username(self):
    #     response=self.session.get(self.signed_url,headers=self.headers)
    #     selector=etree.HTML(response.text)
    #     username=selector.xpath('//p[@class="seeting-link-name mt-3"]/text()')
    #     print(username)
    def statement(self,stock):
        page_headers={
            'Referer':'https://caibaoshuo.com/companies/' + stock ,
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
        }
        url="https://caibaoshuo.com/companies/" + stock + "/financial_reports/ttm"
        response=self.session.get(url,headers=page_headers)
        selector=etree.HTML(response.text)
        lists=selector.xpath('//ul[@class="summary-list"]/li/text()')
        for li in lists:
            print(li)
        self.profit.append(lists[0].split("：",1)[0].split(" ",1)[1])
        self.profit_data.append(lists[0].split("：",1)[1])
        self.net_profit.append(lists[1].split("：",1)[0].split(" ",1)[1])
        self.net_profit_data.append(lists[1].split("：",1)[1])
        self.turnover.append(lists[2].split("：",1)[0].split(" ",1)[1])
        self.turnover_data.append(lists[2].split("：",1)[1])
        self.inventory.append(lists[3].split("：",1)[0].split(" ",1)[1])
        self.inventory_data.append(lists[3].split("：",1)[1])
        self.receivable.append(lists[4].split("：",1)[0].split(" ",1)[1])
        self.receivable_data.append(lists[4].split("：",1)[1])
        self.level.append(lists[5].split("：",1)[0].split(" ",1)[1])
        self.level_data.append(lists[5].split("：",1)[1])
        self.quick.append(lists[6].split("：",1)[0].split(" ",1)[1])
        self.quick_data.append(lists[6].split("：",1)[1])
        self.interest.append(lists[7].split("：",1)[0].split(" ",1)[1])
        self.interest_data.append(lists[7].split("：",1)[1])
        self.cash_ratio.append(lists[8].split("：",1)[0].split(" ",1)[1])
        self.cash_ratio_data.append(lists[8].split("：",1)[1])
        self.cash.append(lists[9].split("：",1)[0].split(" ",1)[1])
        self.cash_data.append(lists[9].split("：",1)[1])


if __name__ == "__main__":
    login = Login()
    login.login('18080072071')
    
    df=pd.read_csv('./data/company.csv',encoding='gb2312')
    stock_codes=list(df.ts_code)

    for code in stock_codes:
        login.statement(code[0:6])
    out={
        "stock_codes":stock_codes,
        "profit":login.profit,
        "profit_data":login.profit_data,
        "net_profit":login.net_profit,
        "net_profit_data":login.net_profit_data,
        "turnover":login.net_profit,
        "turnover_data":login.net_profit_data,
        "inventory":login.inventory,
        "inventory_data":login.inventory_data,
        "receivable":login.receivable,
        "receivable_data":login.receivable_data,
        "level":login.level,
        "level_data":login.level_data,
        "quick":login.quick,
        "quick_data":login.quick_data,
        "interet":login.interest,
        "interet_data":login.interest_data,
        "cash_ratio":login.cash_ratio,
        "cash_ratio_data":login.cash_ratio_data,
        "cash":login.cash,
        "cash_data":login.cash_data
    }
    df=pd.DataFrame(out)
    df.to_csv('./data/statement.csv',mode='a',encoding='gb2312',index=False,header=False)
