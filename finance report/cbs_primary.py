import requests
from lxml import etree
import re
import pandas as pd
import time
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
          #  'Referer':'https://caibaoshuo.com/companies/' + stock[0:6] ,
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
        }
        url="https://caibaoshuo.com/companies/" + stock[:6] 
        response=self.session.get(url,headers=page_headers)
        selector=etree.HTML(response.text)
        lists_data=selector.xpath('//table[contains(@class,table)]//span/text()')
        lists_ratio=selector.xpath('//table[contains(@class,table)]//span/@title')
        data=[stock]
        i=0
        for span in lists_ratio:
            data.append(span)
            data.append(lists_data[i])
            #print(span)
            #print(lists_data[i])
            i=i+1
        return data
if __name__ == "__main__":
    login = Login()
  #  login.login('18080072071')
    
    df=pd.read_csv('./data/company.csv',encoding='gbk')
    stock_codes=list(df.ts_code)
    stock_codes=stock_codes[1111:]
    count=0
    for code in stock_codes:
        out=[]
        result=[]
        result=login.statement(code)
        out.append(result)
        df=pd.DataFrame(out)
        df.to_csv('./data/ratio.csv',mode='a',encoding='gbk',index=False,header=False)
        count=count+1
        time.sleep(1)
        print("进度：" + str(count) + "/" + str(len(stock_codes))+"    当前代码:" + code)

