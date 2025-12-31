# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

from collections import namedtuple
from enum import Enum

LOG_PREFIX = "[ {} ] [ {} ] [ {} ] [ {} ]"
LOG_FORMAT = "{} {}"

Error = namedtuple('Error', ['code', 'message'])
PROJECT_NOT_FOUND = "Project not found"
JENKINSJOBERRORCODE = 2824
DATASET_EXIST_ERROR = "Dataset with same name and version already exists"
USERLIST_ERROR="Userlist is required when scope is restricted"
DATASET_NOT_FOUND_ERROR="Dataset not found"
DATASET_DATA_NOT_EMPTY_ERROR="Dataset data should not be empty"
MODALITY_NOT_EMPTY_ERROR="Modality should not be empty"
UPDATE_DATASET_ERROR="Name and version cannot be changed"
TAGS_NOT_EMPTY_ERROR="Tags should not be empty"

class ErrorCode(Enum):
    PROJECT_NOT_FOUND_ERROR = Error(2820, PROJECT_NOT_FOUND)
    DATASET_NOT_FOUND_ERROR = Error(2821, DATASET_NOT_FOUND_ERROR)
    DATASET_EXIST_ERROR = Error(2801, DATASET_EXIST_ERROR)
    USERLIST_ERROR=Error(2802,USERLIST_ERROR)
    DATASET_DATA_NOT_EMPTY_ERROR=Error(2803,DATASET_DATA_NOT_EMPTY_ERROR)
    MODALITY_NOT_EMPTY_ERROR=Error(2804,MODALITY_NOT_EMPTY_ERROR)
    UPDATE_DATASET_ERROR=Error(2805,UPDATE_DATASET_ERROR)
    TAGS_NOT_EMPTY_ERROR=Error(2806,TAGS_NOT_EMPTY_ERROR)