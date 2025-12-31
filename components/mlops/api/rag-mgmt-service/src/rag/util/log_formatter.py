# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

"""Log Formatter will prettify every log message into standard format ."""

LOG_PREFIX = "[ {} ] [ {} ] [ {} ] [ {} ]"
LOG_FORMAT = "{} {}"
class LogFormatter():
    '''
    Display log in the standard format
    '''

    def __init__(self, service_name:str=""):
        '''
        Initialize log and default params
        '''
        self.service_name = service_name
        self.api_name = ""
        self.sender_uri = ""
        self.request_id = ""
        self.prefix = ""

    def set_prefixes(self, api_name: str = "", sender_uri: str = "", request_id=""):
        '''
        takes all the needed log prefix and make it a sentence
        '''
        self.api_name = api_name
        self.sender_uri = sender_uri
        self.request_id = request_id
        self.prefix = LOG_PREFIX.format(
            self.service_name, self.api_name, self.sender_uri, self.request_id)

    def get_msg(self, message: str):
        '''
        convert the message into a standard format
        '''
        return LOG_FORMAT.format(self.prefix, message)
