import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

chromedriver_path = ''  # 크롬드라이버 실행 경로
driver = webdriver.Chrome(chromedriver_path)

driver.get('https://www.foodsafetykorea.go.kr/portal/specialinfo/searchInfoProduct.do?menu_grp=MENU_NEW04&menu_no=2815')

time.sleep(10)

search_box = driver.find_element(by='prd_cd_nm')
search_box.send_keys('소스')
time.sleep(3)

search_box.send_keys(Keys.ENTER)
# https://coding-kindergarten.tistory.com/24