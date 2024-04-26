# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: utility_service.py
description: Service details for aicloud utility operations

"""

from bson.objectid import ObjectId
from utilities.config.logger import CustomLogger
from utilities.mappers.idp_job_response import ESBulkData
from datetime import datetime
from bson.objectid import ObjectId
import pydantic
import re
import os
import requests
from urllib.parse import urlsplit
import os
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import time
import calendar
from utilities.constants.util_constants import *
from requests.auth import HTTPBasicAuth
import json
from fastapi.encoders import jsonable_encoder


class UtilityService:

    def __init__(self,app):
        self.log = app.logger
        self.db=app

    # Method to pushdata to elasticsearch
    def pushDatatoES(self,esdata: ESBulkData):
        self.log.info('pushDatatoES')
        res={}

        # es_host = ${ES_HOST}
        # es_port = ${ES_PORT}
        # es_scheme = ${ES_SCHEME}
        # es_username = ${ES_USERNAME}
        # es_password = ${ES_PASSWORD}

        es_host = os.getenv("ES_HOST")
        es_port = os.getenv("ES_PORT")
        es_scheme = os.getenv("ES_SCHEME")
        es_username = os.getenv("ES_USERNAME")
        es_password = os.getenv("ES_PASSWORD")

        es_indexName= esdata.esindex
        data= esdata.data

        if data !=None and len(data)==0:
            res["status"]="Failure"
            res["message"]="ES Bulk Data is empty."
        elif  data !=None and len(data)>0:
            try:
               _elasticsearch = Elasticsearch([{'host': str(es_host), 'port': int(es_port), 'scheme': str(es_scheme)}], basic_auth = (str(es_username), str(es_password)),verify_certs=False)

               bulk_data=[]

               for item in data:
                   item["@timestamp"]=datetime.utcnow()
                   bulk_data.append({"_index": es_indexName,"_source": item})

               self.log.info("ES Data ********")
               self.log.info(bulk_data)
               self.log.info("ES Data ********")
               if len(bulk_data)>0:
                    uploadData = bulk(_elasticsearch,bulk_data)
               else:
                   self.log.info("empty data")

               res["status"]="Success"
               res["message"]="Data pushed into ES successfully"
            except(Exception) as e:
                self.log.error(e)
                res["status"]="Failure"
                res["message"]="Some error occurred while pushing data ito ES"
                return res
        return res

    # Method to search in elasticsearch index with modality
    def searchDataES(self,modality:str,reqType:str, body:dict):
        self.log.info('searchDataES')
        start_time = time.time()
        date = datetime.utcnow()
        utc_time = calendar.timegm(date.utctimetuple())
        date_time_stamp = datetime.fromtimestamp(utc_time).strftime("%Y-%m-%d %I:%M:%S %p")
        res={}

        es_username = os.getenv("ES_USERNAME")
        es_password = os.getenv("ES_PASSWORD")

        try:
            modality=modality.upper()
            # indexName=os.getenv(modality+"_INDEX_NAME")

            if modality == "CODE":
                indexName = os.getenv("CODE_ES_INDEX")
            elif modality== "TEXT":
                indexName = os.getenv("TEXT_ES_INDEX")
            else:
                indexName = os.getenv("EMBEDDING_ES_INDEX")

            print("***indexName***",indexName)
            # url=os.getenv("EVAL_ES_INDEX_NAME").replace(INDEX_PLACEHOLDER,indexName)+"/_search"
            esUrl=os.getenv("ES_SCHEME")+"://"+os.getenv("ES_HOST")+":"+os.getenv("ES_PORT")+"/{index}"
            url= esUrl.replace(INDEX_PLACEHOLDER,indexName) + "/"+ reqType
            body = jsonable_encoder(body)
            # response = requests.get(url)
            response = requests.get(url, auth = HTTPBasicAuth(str(es_username), str(es_password)),verify=False, json=body)
            res['status']="Success"
            res['data']=response.json()
        except(Exception) as e:
                self.log.error(e)
                res["status"]="Failure"
                res["message"]="Some error occurred while pushing data ito ES"
                return res
        return res