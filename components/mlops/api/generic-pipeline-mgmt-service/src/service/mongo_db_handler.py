# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
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
        logger.info(connection_string)
        client = MongoClient(connection_string)
        db = client[db_name]
        logger.info(f'Connected to database:{db_name}')

        logger.info(f'db.name={db.name}')
        logger.info(f'db.my_collection={db.my_collection}')

        self.__client = client
        self.__db = db

    # Function to disconnect from the database
    def disconnect(self):
        # Close the connection
        self.__client.close()
        logger.info(f'Connection closed')

    # Function to insert a document
    def insert_document(self, collection_name, data):
        collection = self.__db[collection_name]
        obj = collection.insert_one(data)
        logger.info(obj)
        return obj.inserted_id

    # Function to get a document
    def get_document(self, collection_name, query={}):
        collection = self.__db[collection_name]
        result = collection.find_one(query, {'_id': False})
        return result

    # Function to get all documents
    def get_documents(self, collection_name, filter={}):
        collection = self.__db[collection_name]
        print('Count of items in collection', collection.count_documents({}))
        documents = collection.find(filter)
        return documents

    # Function to get all documents without id
    def get_documents_without_id(self, collection_name, filter={}):
        collection = self.__db[collection_name]
        print('Count of items in collection', collection.count_documents({}))
        print(filter)
        documents = collection.find(filter, {'_id': False})
        return documents

    # Function to update a document
    def update_document(self, collection_name, filter, newvalues):
        collection = self.__db[collection_name]
        update_obj = collection.update_one(filter, newvalues)
        return update_obj.acknowledged