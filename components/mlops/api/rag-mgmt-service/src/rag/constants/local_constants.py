# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""
fileName: local_constants.py
description: Local constants for usecase  module
"""
from collections import namedtuple
from enum import Enum

LOG_PREFIX = "[ {} ] [ {} ] [ {} ] [ {} ]"
LOG_FORMAT = "{} {}"


Error = namedtuple('Error', ['code', 'message'])
PROJECT_NOT_FOUND = "Project not found"
NAME_NOT_EMPTY_ERROR = "Name should not be empty"
PIPLN_NAME_SPECIAL_CHARS_ERROR = "Name should not contain special characters"
DATASET_REQUIRED = "Dataset is should not be empty"
COLLECTION_NAME_REQUIRED = "Collection name is should not be empty"
EMBEDDING_MODEL_REQUIRED = "Embedding model is should not be empty"
SEARCH_SVC_INPUT_REQUIRED = "Search service input is should not be empty"
RAG_INDEX_EXIST_ERROR = "Rag index already exists"
INDEX_NOT_FOUND_ERROR = "Index not found"
PIPELINE_ID_REQUIRED = "Pipeline id is should not be empty"
INDEX_NAME_REQUIRED = "Index name is should not be empty"
FILE_NAME_REQUIRED = "File name is should not be empty"
FILE_PATH_REQUIRED = "File path is should not be empty"
PROJECT_ID_REQUIRED = "Project id is should not be empty"
DATA_INSERTION_EXIST_ERROR = "Record already exists"
PIPELINE_NOT_FOUND_ERROR = "Pipeline not found"
INDEX_DELETE_ERROR = "Index not deleted"
PIPELINE_EXECUTION_ERROR = "Pipeline execution failed"
SEARCH_NOT_FOUND_ERROR = "Search Details not found"
JENKINSJOBERRORCODE = 2824
 
class ErrorCode(Enum):
    PROJECT_NOT_FOUND_ERROR = Error(2801, PROJECT_NOT_FOUND)
    NAME_NOT_EMPTY_ERROR = Error(2802, NAME_NOT_EMPTY_ERROR)
    PIPLN_NAME_SPECIAL_CHARS_ERROR = Error(2803, PIPLN_NAME_SPECIAL_CHARS_ERROR) 
    DATASET_REQUIRED = Error(2804, DATASET_REQUIRED)   
    COLLECTION_NAME_REQUIRED = Error(2805, COLLECTION_NAME_REQUIRED)
    EMBEDDING_MODEL_REQUIRED = Error(2806, EMBEDDING_MODEL_REQUIRED)
    SEARCH_SVC_INPUT_REQUIRED = Error(2807, SEARCH_SVC_INPUT_REQUIRED)
    RAG_INDEX_EXIST_ERROR = Error(2808, RAG_INDEX_EXIST_ERROR)
    INDEX_NOT_FOUND_ERROR = Error(2809, INDEX_NOT_FOUND_ERROR)
    PIPELINE_ID_REQUIRED = Error(2810, PIPELINE_ID_REQUIRED)
    INDEX_NAME_REQUIRED = Error(2811, INDEX_NAME_REQUIRED)
    FILE_NAME_REQUIRED = Error(2812, FILE_NAME_REQUIRED)
    FILE_PATH_REQUIRED = Error(2813, FILE_PATH_REQUIRED)
    PROJECT_ID_REQUIRED = Error(2814, PROJECT_ID_REQUIRED)
    DATA_INSERTION_EXIST_ERROR = Error(2815, DATA_INSERTION_EXIST_ERROR)
    PIPELINE_NOT_FOUND_ERROR = Error(2816, PIPELINE_NOT_FOUND_ERROR)
    INDEX_DELETE_ERROR = Error(2817, INDEX_DELETE_ERROR)
    PIPELINE_EXECUTION_ERROR = Error(2818, PIPELINE_EXECUTION_ERROR)
    SEARCH_NOT_FOUND_ERROR = Error(2819, SEARCH_NOT_FOUND_ERROR)