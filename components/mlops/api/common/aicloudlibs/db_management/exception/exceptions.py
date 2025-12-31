# ===============================================================================================================#
# Copyright 2024 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

import sys, traceback

class AicloudDBException(Exception):
    """
    Abstract base class of all Aicloud DB exceptions.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)