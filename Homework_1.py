""" PyETL作業
1.爬PTT任一個版的圖片並儲存
"""
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import requests
from urllib import request
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15'}

# 列表頁抓標題和網址
page = 1552
catch_page = 3
for i in range(0,catch_page):
    url = 'https://www.ptt.cc/bbs/KoreaStar/index%d.html' % (page)
#    url = 'https://www.ptt.cc/bbs/KoreaStar/index1551.html'
    print(url)

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    # print(soup)
    titles = soup.select('div[class="title"] a')
    for title in titles:
        each_title = title.text
        each_url = 'https://www.ptt.cc' + title['href']
        print(each_title, each_url)

        res = requests.get(each_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        pic_cont = soup.select('div[id="main-content"] a')
        for n in pic_cont:
            pic_url = n['href']
            if pic_url[-3:] == 'jpg' or pic_url[-3:] == 'png':
                request.urlretrieve(pic_url, r'E:\PyETL\homework\ptt\%s' %(pic_url.split('/')[-1]))  # 設定圖片存放位置
                print('已存檔:', pic_url)
    print()
    page -= 1
