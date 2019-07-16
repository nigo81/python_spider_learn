import requests
import pandas as pd 
import time 
import re
from lxml import etree

class Forum(object):
    def __init__(self):
        self.session=requests.Session()
        #self.path="./chenyiwei.csv"
    def cookies_load(self,filepath="./python_spider_learn/chenyiwei/cookies.txt"):
        f = open(filepath, 'r')
        cookies = {}
        for line in f.read().split(';'): 
            name, value = line.strip().split('=', 1)
            cookies[name] = value
        f.close()
        self.cookies=cookies
    def calc_pages(self):
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
            'Referer':'https://bbs.esnai.com/forum-7-1.html'
            
        }
        url='https://bbs.esnai.com/forum-7-1.html'
        response=self.session.get(url,headers=headers,cookies=self.cookies)
        html=etree.HTML(response.text)
        pages=html.xpath('//a[@class="last"]/text()')
        pages=pages[0].split("... ",1)[1]
        self.pages=pages
    def list_page(self,num):
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        #    'Referer':'https://bbs.esnai.com/forum-7-1.html'
        }
        url='https://bbs.esnai.com/forum-7-' + str(num) + '.html'
        response=self.session.get(url,headers=headers,cookies=self.cookies)
        html=etree.HTML(response.text)
        link=html.xpath('//th[@class="common"]/a[contains(@class,"xst")]/@href')
        return link
    def content(self,list_url):
        list_contents=pd.DataFrame(columns=['A','B','C','D','E','F','G','H'])
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        #    'Referer':refer_url
        }
        
        for url in list_url:
            count=0
            pattern1="thread-\d+-"
            str1=re.search(pattern1,url).group(0)
            pattern2="-\d+\.html"
            str2=re.search(pattern2,url).group(0)
            response=self.session.get('https://bbs.esnai.com/'+url,headers=headers,cookies=self.cookies)
            html=etree.HTML(response.text)
            author=html.xpath('//div[@class="authi"]/a/text()')
 
            text=html.xpath('//div[@class="pgt"]//a[@class="last"]/text()')
            if text :
                count=int(text[0].split("... ",1)[1])
            if "chenyiwei" in author:
                list_contents=list_contents.append(self.content_info(html))
            else:
                if count!=0:
                    for i in range(2,count):
                        content_url='https://bbs.esnai.com/' +str1+str(i)+str2
                        response_content=self.session.get(content_url,cookies=self.cookies)
                        html=etree.HTML(response.text)
                        author=html.xpath('//div[@class="authi"]/a/text()')
                        if "chenyiwei" in author:
                            list_contents=list_contents.append(self.content_info(html))
        return list_contents

    def content_info(self,html):
        title=html.xpath('//h1/span/text()')
#        title=title.split(" - CPA业务探讨 -  ",1)(0)
        link=html.xpath('//head/link[@rel="canonical"]/@href')
        authors=html.xpath('//div[@class="authi"]/a[@class="xw1"]/text()')
        comment_times=html.xpath('//div[@class="authi"]/em/text()')
        comment_tables=html.xpath('//div[@class="t_fsz"]/table')
        comment_texts=[]
        for table in comment_tables:
            text=table.xpath('string(.)')
            comment_texts.append(text)
        # comment_texts=self.table_texts(comment_tables)
        try:
            question_author=authors[0]
            question_time=comment_times[0].split("发表于 ",1)[1]
            question_text=comment_texts[0]

            row_initial=[]
            row_initial.append(title[0])
            row_initial.append(link[0])
            row_initial.append(question_author)
            row_initial.append(question_time)
            row_initial.append(question_text)
        except  IndexError:
            pass
        else:        
            i=0
            output=pd.DataFrame(columns=['A','B','C','D','E','F','G','H'])
            for author in authors:
                if author=="chenyiwei":
                    try:
                        row=row_initial[:]
                        row.append(author)
                        comment_time=comment_times[i]
                        comment_time=comment_time.split("发表于 ",1)[1]
                        row.append(comment_time)
                        row.append(comment_texts[i])
                        trans=pd.DataFrame(row).T
                        trans.columns=output.columns
                        output=pd.concat([output,trans])
                    except IndexError:
                        pass
                
                i=i+1
            return output             
    def one_page(self,url):
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
            'Referer':'https://bbs.esnai.com/forum-7-6.html'
        } 
        response=self.session.get(url,headers=headers,cookies=self.cookies)      
        html=etree.HTML(response.text)
        return html
            # title=html.xpath('//title//text()')
            # title=title.split("- CPA业务探讨 ",1)[0]
            # question_url=html.xpath('//head/link/@href')





if __name__ == '__main__':
    forum=Forum()
    forum.cookies_load()
#    forum.calc_pages()
#    print(forum.pages)
    for i in range(1000,0,-1):
        url=forum.list_page(i)
        df=forum.content(url)
        df.to_csv('./data/chenyiwei.csv',encoding='GB18030',index=False,header=False,mode='a')
        print('目前第'+ str(i) + '页，进度为' + str(round((1000-i)/10,2)) + '%')

 