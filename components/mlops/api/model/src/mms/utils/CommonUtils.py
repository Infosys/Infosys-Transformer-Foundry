# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

from requests.models import PreparedRequest
import re

#to check the given URL is valid or not
def check_url(url):
    regex = re.compile(
        r'^(?:http)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return (re.match(regex, url) is not None)

#to check an object to be not none
def checkIfNotNull(obj) :
    if obj is not None :
        return True
    else :
        return False

#To check an ojbect is none
def checkIfNull(obj) :
    if obj is None :
        return True
    else :
        return False

#To check an object not to be an empty
def checkIfNotEmpty(obj) :
    if obj is not None and len(str(obj))>0:
        return True
    else :
        return False

#To check an object to be an empty
def checkIfEmpty(obj) :
    if obj is not None and len(str(obj))<1:
        return True
    else :
        return False

#To check an email ID is valid or not
def checkEmail(email):
    regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
    if re.fullmatch(regex, email):
        return True
    else:
        return False
