import schedule
import time
import datetime
import fruits_crawling
import pymongo_tut
import elastic


def crawlingFuc():
    time_stamp()
    print("Scheduler :: Start")
    crawling_result, elastic_result = 0, 0
    elastic_result = elastic.elastic_check()  # 1 success , 0 false
    crawling_result = fruits_crawling.crawlingStart()  # fruits_crawling start
    if crawling_result == 1 and elastic_result == 1:  # 1 is sucess
        pymongo_tut.mongoa()  # start mongo_save
        elastic.es_import()
    else:
        print("크롤링 스케줄러..실패...")


def time_stamp():
    this_time = time.strftime('%Y.%m.%d - %H:%M:%S')
    print("this_time : ", str(this_time))


def scheduler():
    print("최초실행 시작 ....")
    crawlingFuc()
    print("스케줄러가 시작됩니다")
    schedule.every().hour.do(time_stamp)  # 한시간에 한번씩
    schedule.every().day.at("02:30").do(crawlingFuc)


scheduler()
while True:
    schedule.run_pending()
    time.sleep(1)
