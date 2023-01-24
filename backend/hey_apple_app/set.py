from pymongo import MongoClient
import os 
from elasticsearch import Elasticsearch, helpers 

es = Elasticsearch(
        hosts=['localhost'],
        http_auth=('user','pass')
    )


def search_result():
    docs = es.search(
            index = 'apple' , 
            # body = {
            #     "query" : {
            #         "multi_match" : {
            #             "query" : r_text,
            #             "fields" : ["Category","Title", "Writer","Bookmade"]
            #         }
            #     }
            # }
        )
    # result_dic = {}
    # e_result = []
    # for data in docs['hits']['hits']: 
    #     e_result.append(
    #         {
    #             "Category" : data["_source"]["Category"],
    #             "Title" : data["_source"]["Title"],
    #             "Writer" : data["_source"]["Writer"],
    #             "Bookmade" : data["_source"]["Book_made"],
    #             "Sellprice" : data["_source"]["Sell_price"],
    #             "ImageUri" : data["_source"]["Image_uri"]
    #         }
    #     )
    # result = [e_result[0]]

    result_dic = {
        "result" : docs
    }

    return result_dic