import requests
from lxml import etree
import re

data={
    'pageSize':'15',
    'pageNum':'1',
    'method':'indexQuery',
    'queryType':'1',
    'isStock':'00',
    'ascGuid':'00'
}
headers={
   # 'Referer':'http://cmispub.cicpa.org.cn/cicpa2_web/public/query2/1/00.shtml',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko Core/1.70.3676.400 QQBrowser/10.4.3505.400'
}
url='http://cmispub.cicpa.org.cn/cicpa2_web/09/0000010F84968932A9C24E75CAC4EE99.shtml'
response=requests.get(url,headers=headers)
r=response
r.encoding='GBK'
html=etree.HTML(r.text)

partner=html.xpath('//table[@id="detailtb"]/tr[12]/td[4]/a/text()')
tbs=html.xpath('//table[@id="detailtb"]/tr[12]//td/a/text()')
#print(r.text)
print(partner)
# for td in tbs:
#     # td=td.encode(encoding='GB18030')
#     #td=td.decode(encoding='utf-8')
#     print("".join(td))
# print(html.xpath('//*[@id="detailtb"]/tbody[1]/tr[12]/td[4]/a/@href'))

# print(partner)