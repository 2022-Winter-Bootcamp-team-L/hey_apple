
from pymongo import MongoClient
import os
from elasticsearch import Elasticsearch, helpers
import pandas as pd 
import json
from pathlib import Path

# Get mongoDB data
class My_MongoDB() :
    def __init__(self) :
        self.client = MongoClient("mongodb+srv://heyAppleServer:wgSh8tEOQlV8FqaA@heyapple.v9ean7a.mongodb.net/test")

    def Get_Data(self, db, collection) :
        return self.client[db][collection].find({})
            
    def __del__(self) :
        self.client.close()

# Create Elasticsearch index & import  
class My_Elasticsearch() :
    def __init__(self) :
        self.es = Elasticsearch(
        hosts=['elasticsearch'],
        http_auth=('elastic','heyapple123')
        )
        
    def Search(self, _index, _body) :
        return self.es.search(index=_index, body={_body})
    
    def Insert(self, _index, _data) :
        BASE_DIR = Path(__file__).resolve().parent.parent
        mapping_path = os.path.join(BASE_DIR, 'secrets.json')
        with open(mapping_path, 'r') as f: 
            mapping = json.load(f)

        self.es.indices.create(index = _index, body = mapping)
        helpers.bulk(self.es, _data, index = _index)


def es_import() :
    mongodb = My_MongoDB()
    mongo_data = pd.DataFrame(mongodb.Get_Data("heyapple", "fruits_data"))
    # del(mongo_data['_id'])
    data = mongo_data.to_dict('records')
    print('data : ',data)
    es = My_Elasticsearch()
    es.Insert("apple",data)

def elastic_check():
    # # elastic search connect
    es = Elasticsearch(
        hosts=['elasticsearch'],
        http_auth=('elastic','heyapple123')
    )

    # check elasitc connect 
    if not es.ping():
        print('connection failed')
    else: 
        print('connection successful')

elastic_check()
es_import()