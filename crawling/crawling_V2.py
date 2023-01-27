from selenium import webdriver
from selenium.webdriver.common.keys import Keys # 키보드 입력용
from selenium.webdriver.common.by import By # find할 타입 지정용
import time # time.sleep용
from datetime import datetime, timedelta
from pymongo import MongoClient

import os
import pandas as pd # csv파일 생성

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium import webdriver
from pyvirtualdisplay import Display
import certifi

ca = certifi.where()

chrome_ops = webdriver.ChromeOptions()
# 원래는 --headless로 시뮬레이션 화면 설정을 꺼놓는게 기본, 하지만 끄게 되면 값이 다르게 크롤링 되는 현상 발생
# chrome_ops.add_argument('--headless') 
# chrome_ops.add_argument('--no-sandbox')
# chrome_ops.add_argument('--disable-gpu')
# chrome_ops.add_argument('--disable-setuid-sandbox')
# chrome_ops.add_argument('--incognito')
# chrome_ops.add_argument('--disable-dev-shm-usage')

# display = Display(visible=0, size=(1420, 1080)) # 여기서 가상화면을 실행시키기 때문에 --headless 설정 안해도 됨
# display.start()

driver = webdriver.Chrome(options=chrome_ops)
driver.get('https://www.nongnet.or.kr/front/M000000048/content/view.do')


conn_str = "mongodb+srv://heyAppleServer:wgSh8tEOQlV8FqaA@heyapple.v9ean7a.mongodb.net/test"
try:
    mongo_client = MongoClient(conn_str, tlsCAFile = ca)
    print('mongodb 연결 완료')
except Exception:
    print("Mongodb Error" + Exception)


def next_fruit_v2(num):
    fruit_name = ['사과','배','포도','감귤','바나나','키위','파인애플','오렌지','레몬','망고','단감','아보카도']

    main_search_ip = driver.find_element(By.XPATH, # 1. 메인 페이지의 검색창 클릭
        r'//*[@id="topFixArea"]/div/ul/li[4]/input')
    main_search_ip.send_keys(Keys.ENTER)
    time.sleep(0.5)

    fruit_search_ip = driver.find_element(By.XPATH, # 2. 과일 종류 검색창 클릭
        r'//*[@id="searchArea"]/div[2]/div[1]/input')
    fruit_search_ip.send_keys(fruit_name[num])
    fruit_search_ip.send_keys(Keys.ENTER)
    time.sleep(0.5)
    
    main_search_ip = driver.find_element(By.XPATH, # 1. 메인 페이지의 검색창 클릭
        r'//*[@id="searchArea"]/div[2]/div[1]/button')
    main_search_ip.send_keys(Keys.ENTER)
    time.sleep(0.5)



def get_info_v2(num):
    eng_name = ['Apple','Pear','Grape','Mandarine','Banana','Kiwi','Pineapple','Orange',
    'Lemon','Mango','Persimmon','Avocado']
    weight_to_count = [10,10,4,12,0.12,10,1,3,10,1,10,2]

    fruit = eng_name[num]

    fruit_name = driver.find_element(By.XPATH, # 과일 이름 가져오기
        r'//*[@id="content"]/div/div[2]/div/div[2]/div[1]/div[2]/h4').text
    time.sleep(0.5)

    rm_name = fruit_name.split(' ')[1]
    if not (fruit == 'Mandarine' or fruit == 'Orange' or fruit == 'Avocado'):
        rm_name =  driver.find_element(By.XPATH, # 과일 이름 가져오기
            r'//*[@id="content"]/div/div[2]/div/div[2]/div[1]/div[3]/ul/li[3]/p[1]').text
        
    fruit_price = int(rm_name.split('원')[0].replace(',',''))
    result_price = round(round(fruit_price / weight_to_count[num]),-2)
    print('fruit_price : ',fruit_price, ' count : ',weight_to_count[num], ' ',fruit,' : ',result_price)

    # today = datetime.now().strftime('%Y-%m-%d')
    # data_to_csv = {'name': fruit,'avg_price': result_price}

    # for i in range(1,7):
    #     data_to_csv['price'+str(i)] = 
    #     print(i)
    
    return result_price

for num in range(12):
    next_fruit_v2(num)
    get_info_v2(num)

driver.quit()


