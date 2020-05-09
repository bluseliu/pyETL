""" PyETL作業
1.爬PTT任一個版的圖片並儲存
2.爬104人力銀行任意關鍵字，並將公司名稱、職缺、所需技能整理成CSV儲存
"""

# 1.爬PTT任一個版的圖片並儲存

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import requests
import os
from urllib import request
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15'}

path = r'./res_car'
if not os.path.exists(path):
 os.mkdir(path)

page = 5008
catch = int(input('請輸入抓取頁數: '))
for i in range(0,catch):
   url = 'https://www.ptt.cc/bbs/car/index%d.html'%(page)

   res = requests.get(url, headers=headers)
   soup = BeautifulSoup(res.text, 'html.parser')
   title = soup.select('div[class="title"] a')

   for titles in title:
       print('標題: ' + titles.text)

       try:
           sub_url = 'https://www.ptt.cc' + titles['href']
           print('網址: ' + sub_url)
           sub_res = requests.get(sub_url, headers=headers)
           sub_soup = BeautifulSoup(sub_res.text, 'html.parser')
           content = sub_soup.select('div[id="main-content"] a')[1]['href']

           if 'jpg' == content.split('.')[-1]:
               print('圖片:', content)
           print()
           request.urlretrieve(content,r'./res_car/%s' % (content.split('/')[-1]))  # 設定圖片存放位置

       except:
           pass

   page -= 1



