import schedule
import time
import datetime
import elastic

def crawlingFuc():
    time_stamp()
    print("Scheduler :: elastic Start")
    elastic_result = 0
    elastic_result =elastic.elastic_check() #1 success , 0 false 
    print(elastic_result)
    if elastic_result == 1 : #1 is sucess
        elastic.es_import() #start elastic
    else :
        print("크롤링 스케줄러..실패...")

def time_stamp():
    this_time = time.strftime('%Y.%m.%d - %H:%M:%S')
    print("this_time : " , str(this_time))
    
def scheduler():
    print ("elastic : 스케줄러가 시작합니다")
    schedule.every().hour.do(time_stamp)# 한시간에 한번씩
    schedule.every().day.at("02:25").do(crawlingFuc)


scheduler()
while True:
    schedule.run_pending()
    time.sleep(1)