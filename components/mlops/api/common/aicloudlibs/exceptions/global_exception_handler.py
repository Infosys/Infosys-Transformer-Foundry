# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import os,sys

from fastapi.responses import JSONResponse

from aicloudlibs.constants.http_status_codes import HTTP_STATUS_OK,HTTP_STATUS_NOT_FOUND,HTTP_STATUS_BAD_REQUEST,HTTP_422_UNPROCESSABLE_ENTITY
from aicloudlibs.constants.error_constants import INTEGER_DATATYPE_ERROR,STRING_DATATYPE_ERROR,LIST_DATATYPE_ERROR,\
    BOOLEAN_DATATYPE_ERROR,FLOAT_DATATYPE_ERROR,JSON_DECODE_ERROR,ENUM_VALUE_ERROR

#from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

STATUS="FAILURE"

def validation_error_handler(exc):
    print("inside validation_error_handler")
    print(exc)
    errResp={}
    errdetails=[]
    error1={}
    errResp['status'] = 'FAILURE'
    print(len(exc.errors()))
    for error in exc.errors():
            code=error['type'].split('.')
            print(error['loc'])
            print(code)
            loc_array_len=len(error['loc'])
            print(loc_array_len)
            if code[1]=="integer":
                 code[1]=INTEGER_DATATYPE_ERROR
                 fieldName=error['loc'][loc_array_len-1]
                 error['msg']=fieldName+" "+error['msg']
            elif code[1]=="string":
                 code[1]=STRING_DATATYPE_ERROR
                 fieldName=error['loc'][loc_array_len-1]
                 error['msg']=fieldName+" "+error['msg']
            elif code[1]=="list":
                 code[1]=LIST_DATATYPE_ERROR
                 fieldName=error['loc'][loc_array_len-1]
                 error['msg']=fieldName+" "+error['msg']
            elif code[1]=="bool":
                 code[1]=BOOLEAN_DATATYPE_ERROR
                 fieldName=error['loc'][loc_array_len-1]
                 error['msg']=fieldName+" "+error['msg']
            elif code[1]=="float":
                 code[1]=FLOAT_DATATYPE_ERROR
                 fieldName=error['loc'][loc_array_len-1]
                 error['msg']=fieldName+" "+error['msg']
            elif code[1]=="enum":
                 code[1]=ENUM_VALUE_ERROR
                 fieldnum=error['loc'][loc_array_len-2]
                 if isinstance(fieldnum,int):
                      fieldVal=error['loc'][loc_array_len-3]
                      fieldName=error['loc'][loc_array_len-1]
                      message=fieldVal+"["+str(fieldnum) +"] "+fieldName+" "+error['msg']
                 else:
                      message=fieldName+" "+error['msg']
                 error['msg']=message
            elif code[1]=="jsondecode":
                 code[1]=JSON_DECODE_ERROR
                 error['msg']="json decode error: "+error['msg']
                 
            error1['code']=code[1]
            error1['message']=error['msg']
            print(error1)
            errdetails.append(error1)
    print("************")
    print(errdetails)
    print("************")
    errResp['details']=errdetails
    print(errResp)
    return JSONResponse(
                status_code = HTTP_422_UNPROCESSABLE_ENTITY,
                content = jsonable_encoder(errResp),
            )
    

def  http_exception_handler(exc):
    print(exc)
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(exc.detail),

    )

def unsupported_mediatype_error_handler(exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(exc.detail),

    )




#def my_except_hook(exctype, value, traceback):
    #sys.__excepthook__(exctype, value, traceback)


#sys.excepthook = my_except_hook