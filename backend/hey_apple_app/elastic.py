import pprint
import time
from pymongo import MongoClient
import os
from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import ConnectionError, RequestError
import pandas as pd
import json
from pathlib import Path


# Get mongoDB data

class My_MongoDB():
    def __init__(self):
        self.client = MongoClient(
            "mongodb+srv://heyAppleServer:wgSh8tEOQlV8FqaA@heyapple.v9ean7a.mongodb.net/test")

    def Get_Data(self, db, collection):
        return self.client[db][collection].find({})

    def __del__(self):
        self.client.close()

# Create Elasticsearch index & import


class My_Elasticsearch():
    def __init__(self):
        self.es = Elasticsearch(
            hosts=['http://elasticsearch:9200'],
            http_auth=('elastic', 'heyapple123')
        )

    def Search(self, _index, data=None):
        if data is None:
            data = {"match_all": {}}
        else:
            data = {"match": data}
        body = {"query": data}
        return self.es.search(index=_index, body=body)

    def Insert(self, _index, _data):
        # BASE_DIR = Path(__file__).resolve().parent
        # print(BASE_DIR)
        # mapping_path = os.path.join(BASE_DIR, 'mapping.json')
        with open('/backend/hey_apple_app/mapping.json', 'r') as f:
            mapping = json.load(f)
        try:
            self.es.indices.create(index=_index, body=mapping)
            helpers.bulk(self.es, _data, index=_index)
        except RequestError as ex:
            if ex.error == 'resource_already_exists_exception':
                pass  # Index already exists. Ignore.
            else:  # Other exception - raise it
                raise ex


def es_import():
    mongodb = My_MongoDB()
    mongo_data = pd.DataFrame(mongodb.Get_Data("heyapple", "fruits_data"))
    del (mongo_data['_id'])
    data = mongo_data.to_dict('records')
    elastic = My_Elasticsearch()
    print("#######################################################")
    print("heyapple", data)
    elastic.Insert("heyapple", data)
    print("제발", end="제발")
    data = {"name": "Apple"}
    pprint.pprint(elastic.Search("heyapple", data))


def elastic_check():
    # elastic search connect
    elastic = My_Elasticsearch()

    # check elasitc connect
    connected = False
    while not connected:
        try:
            elastic.es.info()
            connected = True
            print("connected!!!!!!!!!!!!!!!!!!!!")
            return 1
        except ConnectionError:
            print("Elasticsearch not available yet, trying again in 2s...")
            time.sleep(2)
            return 0


elastic_check()
es_import()
