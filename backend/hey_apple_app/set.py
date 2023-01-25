from backend.hey_apple_app.elastic import My_Elasticsearch
from pymongo import MongoClient
import os
from elasticsearch import Elasticsearch, helpers

es = My_Elasticsearch()


def search_result():
    docs = es.search(
        index='heyapple',
        body={
            "query": {
                "multi_match": {
                    "name": "사과"
                }
            }
        }
    )
    result_dic = {}
    e_result = []
    for data in docs['hits']['hits']:
        e_result.append(
            {
                "name": data["_source"]["name"],
                "avg": data["_source"]["avg"],
                "price1": data["_source"]["price1"],
                "date1": data["_source"]["date1"],
                "price2": data["_source"]["price2"],
                "date2": data["_source"]["date2"],
                "price3": data["_source"]["price3"],
                "date3": data["_source"]["date3"],
                "price4": data["_source"]["price4"],
                "date4": data["_source"]["date4"],
                "price5": data["_source"]["price5"],
                "date5": data["_source"]["date5"],
                "price6": data["_source"]["price6"],
                "date6": data["_source"]["date6"],
            }
        )
    result = [e_result[0]]

    result_dic = {
        "result": docs
    }

    return result_dic
