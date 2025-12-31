# ================================================================================================================# 
# ===============================================================================================================# 
# Copyright 2024 Infosys Ltd.                                                                                    # 
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  # 
# http://www.apache.org/licenses/                                                                                # 
# ===============================================================================================================# 

from pydantic import BaseModel
from typing import Any, Dict, List, Sequence


class KeyValuePair(BaseModel):
    __root__: Dict[str, str]


class FlowData(BaseModel):
    nodes: List
    edges: List
    sequence: dict = {}


class PipelineData(BaseModel):
    variables: dict
    globalVariables: dict


class PipelineFormData(BaseModel):
    flowData: FlowData = None
    pipelineData: PipelineData = None
    pipelineId: str
    projectId: str
