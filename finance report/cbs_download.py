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
            'Referer':'https://caibaoshuo.com/companies/' + stock[0:6] ,
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
        }
        url="https://caibaoshuo.com/companies/" + stock[:6] + "/financial_reports/ttm"
        response=self.session.get(url,headers=page_headers)
        selector=etree.HTML(response.text)
        lists=selector.xpath('//ul[@class="summary-list"]/li/text()')
        lists=lists[:10]
        data=[stock]
        i=0
        for li in lists:
            i=i+1
            data.append(li.split("：",1)[0].split(" ",1)[1])
            data.append(li.split("：",1)[1])
        return data
if __name__ == "__main__":
    login = Login()
    login.login('18080072071')
    
    df=pd.read_csv('./data/company.csv',encoding='gb2312')
    stock_codes=list(df.ts_code)
    stock_codes=stock_codes[:10]
    
    count=0
    
    for code in stock_codes:
        out=[]
        result=[]
        result=login.statement(code)
        out.append(result)
        df=pd.DataFrame(out)
        df.to_csv('./data/statement.csv',mode='a',encoding='gb2312',index=False,header=False)
        count=count+1
        print("进度：" + str(count) + "/" + str(len(stock_codes))+"    当前代码:" + code)
