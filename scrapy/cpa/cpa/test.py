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
    'Referer':'http://cmispub.cicpa.org.cn/cicpa2_web/public/query2/1/00.shtml',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko Core/1.70.3676.400 QQBrowser/10.4.3505.400'
}
url='http://cmispub.cicpa.org.cn/cicpa2_web/OfficeIndexAction.do'
response=requests.post(url,data=data,headers=headers)
html=etree.HTML(response.text)

total_pages=html.xpath('//*[@id="pageCtr_basePageDiv"]/a[2]/@href')[0]
total_pages=re.search("(\d+)",total_pages).group(1)
print(total_pages)
print("nigo")
