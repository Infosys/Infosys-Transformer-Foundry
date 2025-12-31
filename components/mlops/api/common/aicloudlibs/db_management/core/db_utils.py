# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

from aicloudlibs.config import config
from aicloudlibs.config.logger import CustomLogger
from motor.motor_asyncio import AsyncIOMotorClient
from aicloudlibs.db_management.core.db_manager import db
import os,sys
from pymongo import MongoClient
import urllib
log=CustomLogger()

BASE_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
mongodb_host=os.getenv("MONGO_DB_HOST")
mongodb_port=os.getenv("MONGO_DB_PORT")
mongodb_userName=os.getenv("MONGODB_USER")
mongodb_password=urllib.parse.quote(os.getenv("MONGODB_PASSWORD"))
db_con_details=os.path.join(BASE_DIR,'database.ini')
db_param=config.readConfig('mongodb',db_con_details)
mongodb_url=db_param['mongodb_url']
mongodb_url=mongodb_url.replace("MONGO_DB_HOST",mongodb_host)
mongodb_url=mongodb_url.replace("MONGO_DB_PORT",mongodb_port)
mongodb_url=mongodb_url.replace("MONGODB_USER",mongodb_userName)
mongodb_url=mongodb_url.replace("MONGODB_PASSWORD",mongodb_password)
database_name=os.getenv("DATABASE_NAME")
max_conn=db_param['maximum_conn_count']
min_conn=db_param['minimum_conn_count']

def connect_mongodb():
     log.info("Enters connect_to_mongo Method: ")
     
     dbclient =MongoClient(mongodb_url)
     log.info("Connected DB Successfully ")
     return dbclient

def get_db(dbclient)->MongoClient:
     print(dbclient)
     return dbclient[database_name]

def close_db_conn(dbclient):
     dbclient.close()