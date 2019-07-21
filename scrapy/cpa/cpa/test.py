import requests
from lxml import etree
import re

data={
    'method':'getPersons',
    'offGuid':'0000010F84968EB0DF50032FB326866C',
    'pageNum':'2',
    'pageSize':'10'
}
headers={
    #'Referer':'http://cmispub.cicpa.org.cn/cicpa2_web/public/query/swszs/%20/0000010F84968EB0DF50032FB326866C.html',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko Core/1.70.3676.400 QQBrowser/10.4.3505.400'
}
url='http://cmispub.cicpa.org.cn/cicpa2_web/07/0000010F849E8B5D4A75C6CE30F00DBE.shtml'
response=requests.get(url)
response.encoding='GBK'
html=etree.HTML(response.text)
#print(response.text)
#test=html.xpath('//table[@id="detailtb"]/tr[3]/node()')[9].text
test=html.xpath('//table[@id="detailtb"]/tr[16]/td[2]/text()')
# print(test)
print(len(data))