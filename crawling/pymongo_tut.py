from pymongo import MongoClient
from pymysql import connect
import pandas as pd
import certifi
ca = certifi.where()


# mongodb 연결
conn_str = "mongodb+srv://heyAppleServer:wgSh8tEOQlV8FqaA@heyapple.v9ean7a.mongodb.net/test"
try:
    mongo_client = MongoClient(conn_str, tlsCAFile = ca)
    print('mongodb 연결 완료')
except Exception:
    print("Mongodb Error" + Exception)

# mysql 연결
try:
    mysql_con = connect(
        host="db",
        user="root",
        password="1234",
        database="mysql-db"
    )
    print('mysql 연결 완료')
except Exception:
    print("Mysql Error" + Exception)



def insert_mongo(): #파일을 읽어 mongodb에 데이터 추가
    
    db = mongo_client['heyapple']
    collection = db['fruits_data']

    file = pd.read_csv("DB_FRUITS.csv", encoding="utf-8")
    print('csv파일 분석')
    collection.insert_many(file.to_dict('records'))
    print('mongodb에 업로드')


def insert_fruit_price():
    mongo_db = mongo_client['heyapple']
    collection = mongo_db['fruits_data']

    fruits = collection.find()
    print('mongodb에서 값 가져오기')    
    mysql_cursor = mysql_con.cursor()

    for data in fruits:
        name = data['name']
        avg = data['avg']
        sql = "UPDATE fruit SET price = %s WHERE name = %s"
        injection = (str(avg),str(name))
        mysql_cursor.execute(sql,injection)
    print('과일 가격 수정')
    mysql_con.commit()
    print('mysql에 저장')
        

    
    mysql_cursor.close()
    mysql_con.close()



print('데이터 업로드를 시작합니다.......')
insert_mongo()
insert_fruit_price()
print('데이터 업로드 종료......')




# db = client["test"]
# collection = db["student"]
# post={"_id":0,"name":"kailash joshi tutorials"}
# result = collection.find()
# for result in result:
#     print(result)








#  print(client.list_database_names())