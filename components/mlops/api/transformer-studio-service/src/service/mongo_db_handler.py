# ================================================================================================================# 
# ===============================================================================================================# 
# Copyright 2024 Infosys Ltd.                                                                                    # 
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # 
# http://www.apache.org/licenses/                                                                                # 
# ===============================================================================================================# 

from pymongo import MongoClient
from bson.objectid import ObjectId
from common.ainauto_logger_factory import AinautoLoggerFactory

logger = AinautoLoggerFactory().get_logger()


class MongoDbHandler():

    def __init__(self, db_host, db_port, db_name, db_username, db_password):
        connection_string = f"mongodb://{db_username}:{db_password}@{db_host}:{db_port}/?authMechanism=DEFAULT"
        # logger.info(connection_string)
        client = MongoClient(connection_string)
        db = client[db_name]
        logger.info(f'Connected to database:{db_name}')

        logger.info(f'db.name={db.name}')
        logger.info(f'db.my_collection={db.my_collection}')

        self.__client = client
        self.__db = db

    def disconnect(self):
        # Close the connection
        self.__client.close()
        logger.info(f'Connection closed')

    def insert_document(self, collection_name, data):
        collection = self.__db[collection_name]
        obj = collection.insert_one(data)
        logger.info(obj)
        return obj.inserted_id

    def get_document(self, collection_name, query={}, projection={'_id': False}):
        collection = self.__db[collection_name]
        result = collection.find_one(
            query, projection)
        # print(type(result))
        return result

    def get_documents(self, collection_name, filter={}):
        collection = self.__db[collection_name]
        print('Count of items in collection', collection.count_documents({}))
        documents = collection.find(filter)
        return documents
        # Process the documents
        # for document in documents:
        #     logger.info(f'inside loop')
        #     logger.info(document)

    def update_document(self, collection_name, filter, newvalues):
        collection = self.__db[collection_name]
        update_obj = collection.update_one(filter, newvalues)
        return update_obj.acknowledged
    
    # Adding new users or changing date for a user in the db.
    def add_user(self, collection_name, data):
        collection = self.__db[collection_name]
        obj = collection.insert_one(data)
        return obj
    
    def add_users(self, collection_name, data):
        collection = self.__db[collection_name]
        obj = collection.insert_many(data)
        return obj
    
    def update_user(self, collection_name, filter, newvalues):
        collection = self.__db[collection_name]
        update_obj = collection.update_one(filter, newvalues)
        return update_obj