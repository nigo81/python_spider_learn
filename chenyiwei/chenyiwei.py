# ------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# Name: chenyiwei.py
# Email:w-wc@foxmail.com
# Author: wwcheng
# Last Modified: 2019-05-09 08:13
# Description:
# ------------------------------------------------------------------------------
import requests
import random
import time
import csv
import re
import os
import sys
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def cookies_load(filepath):
    f = open(filepath, 'r')
    cookies = {}
    for line in f.read().split(';'): 
        name, value = line.strip().split('=', 1)
        cookies[name] = value
    f.close()
    return cookies


def get_one_page(url):
    try:
        user_agent = [
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
        ]
        cookies = cookies_load(r'cookies.txt')
        headers = {'User-Agent': random.choice(user_agent)}
        response = requests.get(url, headers=headers,
                                cookies=cookies, verify=False)
        response.encoding = 'gbk'  # 'utf-8'
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None


def parse_one_page(html, page, url_join="http://bbs.esnai.com/"):
    regex1 = re.compile("<a href=\"(.*?)&amp;pid=\".*?blank\">.*?</a>")
    link0 = regex1.findall(html, re.S)
    link = []
    for x in link0:
        link.append(urljoin(url_join, x.replace('amp;', '')))  # 合成网址
    regex2 = re.compile("<a href=\".*?&amp;pid=\".*?blank\">(.*?)</a>")
    title = regex2.findall(html, re.S)
    regex3 = re.compile(
        r"<em>.*?(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}).*?</em>", re.S)
    date = regex3.findall(html)
    i = 0
    contentlist = []
    for y in date:
        contentlist.append('链接:'+link[i] + '  标题:'+title[i] + '  日期:'+date[i])
        # csv_write("./chenyiwei.csv", (page,link[i],title[i],date[i]))
        i += 1
    return contentlist


def csv_write(filename, content=()):
    csvFile = open(filename, "a", newline='', encoding='utf-8-sig')
    try:
        writer = csv.writer(csvFile)
        writer.writerow(content)
    finally:
        csvFile.close()


def remove_file(filePath):
    if (os.path.exists(filePath)):
        os.remove(filePath)


def main():
    filePath = "./chenyiwei.csv"
    # remove_file(filePath)
    # csv_write(filePath, ('页码','链接','标题','日期'))
    page = 1
    error = 0
    while page < 101 and error < 6:
        sleeptime = random.randint(2, 5)
        time.sleep(sleeptime)
        url = 'http://bbs.esnai.com/home.php?mod=space&uid=102042&do=thread&view=me&type=reply&order=dateline&from=space&page=%s' % page
        tiezi = parse_one_page(get_one_page(url), page)
        print(tiezi)
        if len(tiezi) != 0:
            print('第%s页ok ^_^' % page)
            page += 1
            error = 0
        else:
            error += 1
            print('第%s页出错第%s次！' % (page, error))


if __name__ == '__main__':
    main()
