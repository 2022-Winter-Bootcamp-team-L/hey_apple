from pymongo import MongoClient
import certifi
ca = certifi.where()

conn_str = "mongodb+srv://heyAppleServer:wgSh8tEOQlV8FqaA@heyapple.v9ean7a.mongodb.net/test"
try:
    client = MongoClient(conn_str, tlsCAFile = ca)
except Exception:
    print("Error" + Exception)

db = client["test"] #test라는 db 생성
collection = db["student"] #student라는 collection 생성
post={"_id":0,"name":"kailash joshi tutorials"} # 저장할 값 생성

req = collection.insert_one(post) #collection에 값 추가

result = collection.find() # 값 조회
for result in result:
    print(result)