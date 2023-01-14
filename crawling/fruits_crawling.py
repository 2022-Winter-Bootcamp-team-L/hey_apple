from selenium import webdriver
from selenium.webdriver.common.keys import Keys # 키보드 입력용
from selenium.webdriver.common.by import By # find할 타입 지정용
import time # time.sleep용

import os
import pandas as pd # csv파일 생성

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException

driver = webdriver.Chrome('./chromedriver2')
driver.get('https://www.nongnet.or.kr/front/M000000048/content/view.do')

fruit = ['사과','배','포도','감귤','바나나','키위','파인애플','오렌지','레몬','망고','단감','아보카도']

def get_info(fruit):
    fruit_name = driver.find_element(By.XPATH, # 과일 이름 가져오기
        r'//*[@id="gdid_selectPummokName"]').text

    if fruit == '망고' or fruit == '아보카도': # 평균 가격 가져오기
        price_avg = driver.find_element(By.XPATH, # 망고, 아보카도만 예외
            r'//*[@id="gcid_itemList"]/div/div/div/ul/li[1]/a/div/div/div/p/span/b').text
    else :    
        price_avg = driver.find_element(By.XPATH, # 평균 가격
            r'//*[@id="gcid_itemList"]/div/div/div[2]/ul/li[1]/a/div/div/div/p/span/b').text

    price_trend = driver.find_elements(By.XPATH, # 6일 전까지 가격
        r'//*[@id="selectDayTrendWithGubun"]/div/div/div[2]/ul')
    
    fruit_data = { 'name': fruit_name, 'price': price_avg} # 크롤링 데이터 초기화
    # fruit_data = {}
    # fruit_data['name'] = fruit_name
    # fruit_data['price'] = price_avg # 다른 방식 초기화

    date = '' # N일 전 날짜 
    won = '' # N일 전 날짜 가격
    i = 0 # 줄마다 해주어야 하는 동작이 다르기 때문에 줄 구분용 변수
    
    for info in price_trend: # li를 돌면서 
        arr = info.text.split('\n')
        for text in arr:
            if i%3 == 0:
                date = text
            elif i%3 == 1: # 가격만 남도록 파싱
                temp = text.split('톤')[1]
                won = temp.split('원')[0]
            else :
                print(date," : ",won)
                fruit_data[date] = won # { '날짜' : '가격' }
            i += 1
    
    frame = pd.DataFrame([fruit_data])
    csv = 'DB_FRUITS.csv'
    if not os.path.exists(csv): # 파일 생성 로직
        frame.to_csv(csv, index=False, mode='w', encoding='utf-8-sig')
    else:
        frame.to_csv(csv, index=False, mode='a', encoding='utf-8-sig', header=False)
    time.sleep(3)

def next_fruit(fruit):

    main_search_ip = driver.find_element(By.XPATH, # 1. 메인 페이지의 검색창 클릭
        r'//*[@id="content"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/button')
    main_search_ip.send_keys(Keys.ENTER)
    time.sleep(0.5)
    fruit_search_ip = driver.find_element(By.XPATH, # 2. 과일 종류 검색창 클릭
        r'//*[@id="settingTab01"]/div[2]/input')
    fruit_search_ip.send_keys(fruit)
    fruit_search_ip.send_keys(Keys.ENTER)
    time.sleep(0.5)

    fruit_enter_bt = driver.find_element(By.XPATH, # 3. 과일 종류 검색 버튼 클릭
        r'//*[@id="settingTab01"]/div[2]/button')
    fruit_enter_bt.send_keys(Keys.ENTER)
    time.sleep(0.5)

    fruit_item_lb = driver.find_element(By.XPATH, # 4. 과일 종류 선택창에서 품목 라벨 클릭
        r'//*[@id="mCSB_1_container"]/ul/li')
    lb = fruit_item_lb.find_element(By.TAG_NAME,'label')
    driver.execute_script('arguments[0].click();',lb) #얘는 왠지 .click 동작 안함, script로 강제 실행
    time.sleep(0.5)    

    fruit_save_bt = driver.find_element(By.XPATH, # 5. 저장 버튼 클릭
        r'//*[@id="settingArea"]/ul/li[2]/button')
    fruit_save_bt.send_keys(Keys.ENTER)
    time.sleep(0.5)




for name in fruit:
    next_fruit(name)
    get_info(name)



