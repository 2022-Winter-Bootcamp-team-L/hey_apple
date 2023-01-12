from pymongo import MongoClient
import certifi
ca = certifi.where()

conn_str = "mongodb+srv://heyAppleServer:wgSh8tEOQlV8FqaA@heyapple.v9ean7a.mongodb.net/test"
try:
    client = MongoClient(conn_str, tlsCAFile = ca)
except Exception:
    print("Error" + Exception)

db = client["test"]
collection = db["student"]
post={"_id":0,"name":"kailash joshi tutorials"}
result = collection.find()
for result in result:
    print(result)








#  print(client.list_database_names())