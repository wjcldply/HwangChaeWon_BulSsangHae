import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time


# Setup options
option = Options()
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

time.sleep(30)

end_page_num = 11
for i in range(1, end_page_num):
    browser.find_element(By.XPATH, '//*[@id="contents"]/main/section/div[2]/div[3]/div/ul/li[7]').click()
    time.sleep(20)
