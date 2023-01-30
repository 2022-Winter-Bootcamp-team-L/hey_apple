import schedule
import time
import datetime
import fruits_crawling
import pymongo_tut

def crawlingFuc():
    time_stamp()
    print("Scheduler :: crawling Start")
    crawling_result = 0
    crawling_result =fruits_crawling.crawlingStart() # fruits_crawling start
    print(crawling_result)
    if crawling_result == 1 : #1 is sucess
        pymongo_tut.mongoa() #start mongo_save
        

def time_stamp():
    #now = time.localtime()
    this_time = time.strftime('%Y.%m.%d - %H:%M:%S')
    print("this_time : " , str(this_time))
    
def scheduler():
    print("최초실행 시작 ....")
    crawlingFuc()
    
    print ("스케줄러가 시작합니다")
    #schedule.every(5).seconds.do(time_stamp)
    #schedule.every(300).seconds.do(crawlingFuc)
    schedule.every().hour.do(time_stamp)# 한시간에 한번씩
    schedule.every().day.at("02:00").do(crawlingFuc)


scheduler()
while True:
    schedule.run_pending()
    time.sleep(1)