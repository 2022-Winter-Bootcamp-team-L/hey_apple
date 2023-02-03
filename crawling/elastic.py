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
            hosts=['http://elasticsearch:9200']
            # http_auth=('elastic', 'heyapple123')
        )

    def Search(self, _index, data=None):
        if data is None:
            data = {"match_all": {}}
        else:
            data = {"match": data}
        body = {"query": data}
        return self.es.search(index=_index, body=body)

    def Insert(self, _index, _data):
        with open('/crawling/mapping.json', 'r') as f:
            mapping = json.load(f)
        # try:
        time.sleep(2)
        self.es.indices.delete(index=_index, ignore_unavailable=True)
        time.sleep(2)
        self.es.indices.create(index=_index, body=mapping)
        time.sleep(2)
        helpers.bulk(self.es, _data, index=_index)
        print("task(Insert) All good")


def es_import():
    mongodb = My_MongoDB()
    mongo_data = pd.DataFrame(mongodb.Get_Data("heyapple", "fruits_data"))
    del (mongo_data['_id'])
    data = mongo_data.to_dict('records')
    elastic = My_Elasticsearch()
    elastic.Insert("heyapple", data)
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
            print("elasticsearch connected")
            return 1
        except ConnectionError:
            print("Elasticsearch not available yet, trying again in 2s...")
            time.sleep(2)
            return 0


if __name__ == "__main__":
    elastic_check()
    time.sleep(2)
    es_import()
