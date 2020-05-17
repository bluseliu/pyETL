""" PyETL作業
2.爬104人力銀行任意關鍵字，並將公司名稱、職缺、所需技能整理成CSV儲存
"""

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import requests
import os
from bs4 import BeautifulSoup
import json
import csv

os.chdir(r'E:\PyETL\homework\104')

with open('jobs.csv', 'a', newline='') as csvFile:  # 開啟輸出的 CSV 檔案
    writer = csv.writer(csvFile)  # 建立 CSV 檔寫入器
    writer.writerow(['公司名', '職務名', '語言能力', '技能', '證照', '其他條件'])  # 標題

# 使用關鍵字網址
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
           "Accept": "application/json, text/plain, */*",
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6","Connection": "keep-alive",
           "Cookie": "luauid=820259659; __auc=ef1e8d4516edf2b9874f045d4d4; _hjid=3ac46d6e-93ff-4bb4-9abe-07334d42c3e7; ALGO_EXP_6019=A; _gaexp=GAX1.3.Whge_MYJQ8if_hNhE9xj7A.18481.0; _gid=GA1.3.401601660.1589438874; job_same_ab=2; cust_same_ab=2; bprofile_history=%5B%7B%22key%22%3A%221a2x6bjpjb%22%2C%22custName%22%3A%22%E5%A5%BD%E5%A5%BD%E6%8A%95%E8%B3%87%E7%A7%91%E6%8A%80%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22custLink%22%3A%22https%3A%2F%2Fwww.104.com.tw%2Fcompany%2F1a2x6bjpjb%22%7D%2C%7B%22key%22%3A%2210zxkwmw%22%2C%22custName%22%3A%22%E6%98%8E%E9%99%BD%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22custLink%22%3A%22https%3A%2F%2Fwww.104.com.tw%2Fcompany%2F10zxkwmw%22%7D%2C%7B%22key%22%3A%221a2x6bl7au%22%2C%22custName%22%3A%22%E5%B0%8A%E6%89%BF%E7%A7%91%E6%8A%80%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%20(%E7%B1%8C%E5%82%99%E8%99%95)%22%2C%22custLink%22%3A%22https%3A%2F%2Fwww.104.com.tw%2Fcompany%2F1a2x6bl7au%22%7D%2C%7B%22key%22%3A%221a2x6bjxsx%22%2C%22custName%22%3A%22%E5%9C%96%E9%9D%88%E6%95%B8%E4%BD%8D%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22custLink%22%3A%22https%3A%2F%2Fwww.104.com.tw%2Fcompany%2F1a2x6bjxsx%22%7D%2C%7B%22key%22%3A%2210vcwn74%22%2C%22custName%22%3A%22%E5%8B%95%E5%8A%9B%E5%AE%89%E5%85%A8%E8%B3%87%E8%A8%8A%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22custLink%22%3A%22https%3A%2F%2Fwww.104.com.tw%2Fcompany%2F10vcwn74%22%7D%2C%7B%22key%22%3A%22at8e1vc%22%2C%22custName%22%3A%22%E6%AC%A3%E8%88%88%E9%9B%BB%E5%AD%90%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22custLink%22%3A%22https%3A%2F%2Fwww.104.com.tw%2Fcompany%2Fat8e1vc%22%7D%2C%7B%22key%22%3A%22ab1fryw%22%2C%22custName%22%3A%22%E6%98%8A%E9%9D%92%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%2C%22custLink%22%3A%22https%3A%2F%2Fwww.104.com.tw%2Fcompany%2Fab1fryw%22%7D%5D; __asc=bb8341a8172123543d3f55797cd; _hjAbsoluteSessionInProgress=1; TS016ab800=01180e452dc4b57a533380c774e8c4eb70e8c5fdd7821272e749ab6aee03620b0426eb7b044521179e81b928b90f7c003117ebc7ea818247e8c5d66806a2f4e42d67f9663f9309daaf161ec7545b5684ee26d505e7; _dc_gtm_UA-15276226-1=1; lup=820259659.5001489413863.5035849152215.1.4640712161167; lunp=5035849152215; _ga=GA1.1.934456123.1575702207; _ga_W9X1GB1SVR=GS1.1.1589438873.26.1.1589443883.39; _ga_FJWMQR9J2K=GS1.1.1589438873.23.1.1589443883.0",
           "Host": "www.104.com.tw",
           "Referer": "https://www.104.com.tw/job/2i5xf?jobsource=hotjob_chr",
           "Sec-Fetch-Dest": "empty",
           "Sec-Fetch-Mode": "cors","Sec-Fetch-Site": "same-origin"}

# 總頁數 =====
# 關鍵字=資料科學家
page_url = 'https://www.104.com.tw/jobs/search/?ro=0&keyword=%E8%B3%87%E6%96%99%E7%A7%91%E5%AD%B8%E5%AE%B6&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc'
res = requests.get(page_url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
totalPage = str(soup.select('body[id="job-jobList"][class="job-list-body"] script')[3]).split(',')[-2].split(':')[-1]

# 讀取搜尋結果列表頁
for num in range(1,int(totalPage)+1):
    # url = 'https://www.104.com.tw/jobs/search/?ro=0&keyword=%E8%B3%87%E6%96%99%E7%A7%91%E5%AD%B8%E5%AE%B6&order=1&asc=0&page=1&mode=s&jobsource=2018indexpoc'
    url = 'https://www.104.com.tw/jobs/search/?ro=0&keyword=%E8%B3%87%E6%96%99%E7%A7%91%E5%AD%B8%E5%AE%B6&order=1&asc=0&page=' + str(num) + '&mode=s&jobsource=2018indexpoc'
    print(url)

# 職務頁網址
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    #print(soup)

    links = soup.select('div[class="b-block__left"] a[class="js-job-link"]')
    # print(links)
    for link in range(0, len(links)):
        link = links[link]['href'][21:26]
        # print(link)
        real_url = 'https://www.104.com.tw/job/ajax/content/' + link
        print(real_url)
        res = requests.get(real_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser').decode('utf8')
        # print(soup)
        # soup_1 = json.dumps(soup, ensure_ascii=False, indent=2)
        # print(soup_1)
        js = json.loads(res.text)
        #print(json.dumps(js, ensure_ascii=False, indent=2))

# 取出技能並轉為dict
        skill_list = []
        skill = js["data"]["condition"]["skill"]
        for n in range(0,len(skill)):
            skill_all = skill[n].get('description')
            all_list = skill_list.append(skill_all)
        skill_dict = {"技能":skill_list}

        jobs = {"公司名": str(js["data"]["header"]["custName"]),
                "職務名": str(js["data"]["header"]["jobName"]),
                "語言能力": str(js["data"]["condition"]["language"]),
                "技能": skill_list, # "技能": str(js["data"]["condition"]["skill"])
                "證照": str(js["data"]["condition"]["certificate"]),
                "其他條件": str(js["data"]["condition"]["other"])
                }
        print(jobs)

# 存檔
        os.chdir(r'E:\PyETL\homework\104')
        try:

            with open('jobs.csv', 'a', newline='') as csvFile: # 開啟輸出的 CSV 檔案
                writer = csv.writer(csvFile) # 建立 CSV 檔寫入器
                writer.writerow([jobs.get('公司名'), jobs.get('職務名'), jobs.get('語言能力'), jobs.get('技能'), jobs.get('證照'), jobs.get('其他條件')])
                print('已寫入')
                print()

        except:
            pass

num += 1


"""
from urllib import request
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys

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
