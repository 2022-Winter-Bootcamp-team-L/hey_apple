from selenium import webdriver
from selenium.webdriver.common.keys import Keys # 키보드 입력용
from selenium.webdriver.common.by import By # find할 타입 지정용
import time # time.sleep용

import os
import pandas as pd # csv파일 생성

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium import webdriver
from pyvirtualdisplay import Display

from .pymongo_tut import insert_mongo, insert_fruit_price

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


def next_fruit(num):
    fruit = ['사과','배','포도','감귤','바나나','키위','파인애플','오렌지','레몬','망고','단감','아보카도']


    main_search_ip = driver.find_element(By.XPATH, # 1. 메인 페이지의 검색창 클릭
        r'//*[@id="content"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/button')
    main_search_ip.send_keys(Keys.ENTER)
    time.sleep(0.5)
    fruit_search_ip = driver.find_element(By.XPATH, # 2. 과일 종류 검색창 클릭
        r'//*[@id="settingTab01"]/div[2]/input')
    fruit_search_ip.send_keys(fruit[num])
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




def get_info(num):
    eng_name = ['Apple','Pear','Grape','Mandarine','Banana','Kiwi','Pineapple','Orange',
    'Lemon','Mango','Persimmon','Avocado']
    weight_to_count = [10,10,4,12,0.12,10,1,3,10,1,10,2]

    fruit = eng_name[num]

    # fruit_name = driver.find_element(By.XPATH, # 과일 이름 가져오기
    #     r'//*[@id="gdid_selectPummokName"]').text

    if fruit == 'Mango' or fruit == 'Avocado' or fruit == 'Pear': # 평균 가격 가져오기
        price_avg = driver.find_element(By.XPATH, # 망고, 아보카도, 배만 예외
            r'//*[@id="gcid_itemList"]/div/div/div/ul/li[1]/a/div/div/div/p/span/b').text
    else :    
        price_avg = driver.find_element(By.XPATH, # 평균 가격
            r'//*[@id="gcid_itemList"]/div/div/div[2]/ul/li[1]/a/div/div/div/p/span/b').text

    price_trend = driver.find_elements(By.XPATH, # 6일 전까지 가격
        r'//*[@id="selectDayTrendWithGubun"]/div/div/div[2]/ul')
    
    fruit_data = { 'name': fruit, 'avg': price_avg} # 크롤링 데이터 초기화
    # fruit_data = {}
    # fruit_data['name'] = fruit_name
    # fruit_data['price'] = price_avg # 다른 방식 초기화

    date = '' # N일 전 날짜 
    won = '' # N일 전 날짜 가격
    i = 0 # 줄마다 해주어야 하는 동작이 다르기 때문에 줄 구분용 변수
    id = 1
    for info in price_trend: # li를 돌면서 
        arr = info.text.split('\n')
        print(arr)
        for text in arr:
            if i%3 == 0:
                date_text = text
                date_key = "date"+str(id)
                price_key = "price"+str(id)
                id = id+1
            elif i%3 == 1: # 가격만 남도록 파싱
                print('text----------',text)
                print('i ---------------',i)
                temp = text.split('톤')[1]
                won = temp.split('원')[0]
            else :
                fruit_data[price_key] = won # { 'price0' : '3400' }
                fruit_data[date_key] = date_text #{ 'date0' : '01.14(토 )'}
            i += 1
    print(fruit_data)
    frame = pd.DataFrame([fruit_data])
    csv = 'DB_FRUITS.csv'
    if not os.path.exists(csv): # 파일 생성 로직
        frame.to_csv(csv, index=False, mode='w', encoding='utf-8-sig')
    else:
        frame.to_csv(csv, index=False, mode='a', encoding='utf-8-sig', header=False)
    time.sleep(3)





for num in range(12):
    next_fruit(num)
    get_info(num)

driver.quit()


