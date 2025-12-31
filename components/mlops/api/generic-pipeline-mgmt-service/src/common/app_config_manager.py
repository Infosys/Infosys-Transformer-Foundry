# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import os
import configparser
from dotenv import load_dotenv
from common.common_util import Singleton

loaded = load_dotenv('../.env')
if not loaded:
    raise EnvironmentError

class AppConfigManager(metaclass=Singleton):
    def __init__(self):
        config_files = [os.path.abspath(os.environ.get('CONFIG_PATH'))]
        self.__app_config = self.__get_config_parser(config_files)
    
    # Method to get the configuration parser
    def __get_config_parser(self, config_file):
        config_parser = configparser.ConfigParser()
        config_parser.read(config_file)
        return config_parser

    # Method to get the app configuration
    def get_app_config(self):
        return self.__app_config

    # Method to get the about app
    def get_about_app(self):
        return {
            "service_name": self.__app_config["DEFAULT"]["service_name"],
            "service_version": self.__app_config["DEFAULT"]["service_version"]
        }