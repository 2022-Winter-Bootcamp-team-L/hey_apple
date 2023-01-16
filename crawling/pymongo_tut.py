from pymongo import MongoClient
from pymysql import connect
import pandas as pd
import certifi
ca = certifi.where()



# mongodb 연결
conn_str = "mongodb+srv://heyAppleServer:wgSh8tEOQlV8FqaA@heyapple.v9ean7a.mongodb.net/test"
try:
    mongo_client = MongoClient(conn_str, tlsCAFile = ca)
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
except Exception:
    print("Mysql Error" + Exception)



def insert_mongo(): #파일을 읽어 mongodb에 데이터 추가
    db = mongo_client['heyapple']
    collection = db['fruits_data']

    file = pd.read_csv("DB_FRUITS.csv", encoding="utf-8")
    collection.insert_many(file.to_dict('records'))


def get_price_avg():
    mongo_db = mongo_client['heyapple']
    collection = mongo_db['fruits_data']

    fruits = collection.find()

    mysql_cursor = mysql_con.cursor()

    print(fruits)
    
    # sql = "UPDATE fruit SET price = %s WHERE name = %s"


insert_mongo()





# db = client["test"]
# collection = db["student"]
# post={"_id":0,"name":"kailash joshi tutorials"}
# result = collection.find()
# for result in result:
#     print(result)








#  print(client.list_database_names())