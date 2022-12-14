from pprint import pprint
import requests
from bs4 import BeautifulSoup

import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time


items = []  # save the item infos
last_key = 0  # save the identification number of the last item saved
item_count = 0
filtered_item_count = 0


def table_to_lst(out_lst, in_elements):
    global last_key
    # print(last_key)
    for element in in_elements:
        infos = element.find_elements(By.CLASS_NAME, 'table_txt')
        temp = []  # temporarily save the item infos without sorting
        for info in infos:
            try:
                product = info.find_element(By.CLASS_NAME, 'bssh fancybox.ajax')
                temp.append(product.text)
                # print(product.text)
            except:
                # print(info.text)
                temp.append(info.text)
        new_item = []  # sort the infos from table
        for i in range(len(temp)):
            if len(new_item) != 6:
                new_item.append(temp[i])
            else:
                new_item.append(temp[i])
                if last_key == 0:
                    out_lst.append(new_item)
                    last_key = int(new_item[0])
                elif int(new_item[0]) < last_key:
                    out_lst.append(new_item)
                    last_key = int(new_item[0])
                else:
                    pass
                new_item = []
    # pprint(items)
    return out_lst


f_raw = open('식품_raw.csv', 'w', newline='', encoding='utf-8-sig')
f_filtered = open('식품_filtered.csv', 'w', newline='', encoding='utf-8-sig')
writer = csv.writer(f_raw)
writer2 = csv.writer(f_filtered)


def items_to_csv():
    global items
    global item_count
    writer.writerows(items)
    item_count += len(items)


def check_expiration(lst):  # 유통기한 필터링 
    global filtered_item_count
    new_line = lst
    expiration_date_unformatted = lst[4]
    # '개월' 키워드로 찾기
    idx = expiration_date_unformatted.find('개월')
    if idx == -1:  # '개월' 키워드 존재하지 않을 경우
        # '년' 키워드로 찾기
        idx = expiration_date_unformatted.find('년')
        if idx == -1:  # '년' 키워드 존재하지 않을 경우
            return
        else:
            try:
                digit = int(expiration_date_unformatted[idx-2:idx])
            except:
                digit = int(expiration_date_unformatted[idx-1])
            if digit >= 2:
                new_line[4] = digit
                writer2.writerow(new_line)
                filtered_item_count += 1
                return
    else:
        try:
            digit = int(expiration_date_unformatted[idx-2:idx])
        except:
            digit = int(expiration_date_unformatted[idx-1])
        if digit >= 24:
            new_line[4] = digit
            writer2.writerow(new_line)
            filtered_item_count += 1
            return
        else:
            return
        


# Setup options
option = Options()
option.add_argument('--incognito')
option.add_argument('--window-size=1910x1080')
option.add_argument('disable-infobars')
option.add_argument('disable-extensions')
option.add_argument('disable-gpu')

# Selenium 4.0 - load webdriver
try:
    s = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=s, options=option)
except Exception as e:
    print(e)

# Move to URL
browser.get('https://www.foodsafetykorea.go.kr/portal/specialinfo/searchInfoProduct.do?menu_grp=MENU_NEW04&menu_no=2815')

# wait for the page to load
time.sleep(2)

# Search the items by keyword
search_keyword = '소스'
search_box = browser.find_element(By.ID, 'prd_cd_nm')
search_box.send_keys(search_keyword)

# Choose to show 50 items per load
browser.find_element(By.ID, 'a_list_cnt').click()
browser.find_element(By.XPATH, '//*[@id="contents"]/main/section/div[2]/div[2]/div[2]/div[5]/ul/li[5]/a').click()

# wait for the search result
time.sleep(20)

# save the whole table into <elements>
elements = browser.find_elements(By.ID, 'tbody')

# save the data from table into a list
table_to_lst(items, elements)

items_to_csv()  # 이중 리스트 items에 담긴 정보들을 csv에 저장하는 함수
for item in items:
    check_expiration(item)  # 크롤링한 테이블의 식품 유통기한 필터링하는 함수
items = []  # items 초기화해 리스트 오버플로우 방지하기

# end_page_num = 2221
end_page_num = 3
for i in range(1, end_page_num):
    # load the next page
    browser.find_element(By.XPATH, '//*[@id="contents"]/main/section/div[2]/div[3]/div/ul/li[7]').click()
    # wait for the page to load
    time.sleep(20)

    # save the whole table into <elements>
    elements = browser.find_elements(By.ID, 'tbody')
    # save the data from table into a list
    table_to_lst(items, elements)

    items_to_csv()  # 이중 리스트 items에 담긴 정보들을 csv에 저장하는 함수 작성하기
    for item in items:
        check_expiration(item)  # 크롤링한 테이블의 식품 유통기한 필터링하는 함수
    items = []  # items 초기화해 리스트 오버플로우 방지하기 




# pprint(items)
print('total number of items searched is :' + str(item_count))
print('total number of filtered items is :' + str(filtered_item_count))
f_raw.close()
f_filtered.close()
