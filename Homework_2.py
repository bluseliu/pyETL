# ===================
""" PyETL作業
2.爬104人力銀行任意關鍵字，並將公司名稱、職缺、所需技能整理成CSV儲存
"""
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import requests
import os
from urllib import request
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from time import sleep
import json
import re

"""
# 使用 selenium
driver = Chrome('./chromedriver')
url = 'https://www.104.com.tw/jobs/main/'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
    'Cookie': 'luauid=1767450017; __asc=42c43cc9171dd6b413bc1891199; __auc=42c43cc9171dd6b413bc1891199; _gid=GA1.3.10201509.1588557726; _hjid=7738c069-bac6-4995-ae3d-b56af90ff98e; ALGO_EXP_6019=C; job_same_ab=2; lup=1767450017.4623532291991.5035849152215.1.4640712161167; lunp=5035849152215; TS016ab800=01180e452d7a1007d2684447c6533f8bdf007c67e917a91a364e61c8596583923c6380c78feb31b165fa4a327f7821f58ef490cc859a00c84fc0db914f65a13597ece0845407141c37d78fe2e5871da87fa505b17d; _ga=GA1.1.195299847.1588557726; _ga_W9X1GB1SVR=GS1.1.1588557726.1.1.1588558057.60; _ga_FJWMQR9J2K=GS1.1.1588557726.1.1.1588558057.0'}

driver.get(url)
driver.find_element_by_id('ikeyword').send_keys("") # 清除搜尋輸入框中的內容
driver.find_element_by_id('ikeyword').send_keys('資料科學家') # 在搜尋輸入框中輸入關鍵字
driver.find_element_by_id('ikeyword').send_keys(Keys.RETURN) # 觸發搜尋輸入框的 ENTER 指令
joblist = driver.page_source
# print('joblist:', joblist)
sleep(3)
driver.find_element_by_class_name('b-txt--highlight').click()
htmltext = driver.page_source
# print(htmltext)
soup = BeautifulSoup(driver.page_source, "html.parser")
"""

# 使用關鍵字網址
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
    'Cookie': 'luauid=1767450017; __asc=42c43cc9171dd6b413bc1891199; __auc=42c43cc9171dd6b413bc1891199; _gid=GA1.3.10201509.1588557726; _hjid=7738c069-bac6-4995-ae3d-b56af90ff98e; ALGO_EXP_6019=C; job_same_ab=2; lup=1767450017.4623532291991.5035849152215.1.4640712161167; lunp=5035849152215; TS016ab800=01180e452d7a1007d2684447c6533f8bdf007c67e917a91a364e61c8596583923c6380c78feb31b165fa4a327f7821f58ef490cc859a00c84fc0db914f65a13597ece0845407141c37d78fe2e5871da87fa505b17d; _ga=GA1.1.195299847.1588557726; _ga_W9X1GB1SVR=GS1.1.1588557726.1.1.1588558057.60; _ga_FJWMQR9J2K=GS1.1.1588557726.1.1.1588558057.0'}

url = 'https://www.104.com.tw/jobs/search/?keyword=%E8%B3%87%E6%96%99%E7%A7%91%E5%AD%B8%E5%AE%B6&order=1&jobsource=2018indexpoc&ro=0'
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')


# 一筆資料
"""
links = soup.select('div[class="b-block__left"] a')[0]['href'].split('//www.104.com.tw/job/')[1][:5]
real_url = 'https://www.104.com.tw/job/ajax/content/' + links
print(real_url)
res = requests.get(real_url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser').decode('utf8')
js = json.loads(res.text)
# print(json.dumps(js, ensure_ascii=False, indent=2))
print(js["data"]["header"]["custName"]) # 看公司名(不用轉碼)
"""

# 多筆資料(一頁)
links = soup.select('div[class="b-block__left"] a[class="js-job-link"]')
for link in range(0,len(links)):
    link = links[link]['href'][21:26]
    print(link)
    real_url = 'https://www.104.com.tw/job/ajax/content/' + link
    print(real_url)
    res = requests.get(real_url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser').decode('utf8')
    # print(soup)
   # soup_1 = json.dumps(soup, ensure_ascii=False, indent=2)
    #print(soup_1)
    js = json.loads(res.text)
    print(json.dumps(js, ensure_ascii=False, indent=2))
    """
    print('公司名:', js["data"]["header"]["custName"])  # 看公司名(不用轉碼)
    print('職務名', js["data"]["header"]["jobName"])
    print('語言能力', js["data"]["condition"]["language"])
    print('技能', js["data"]["condition"]["skill"])
    print('證照', js["data"]["condition"]["certificate"])
    print('其他條件', js["data"]["condition"]["other"])
    print()
"""
