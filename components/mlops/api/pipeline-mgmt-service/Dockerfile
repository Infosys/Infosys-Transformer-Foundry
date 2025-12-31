# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

FROM python:3.9
ENV DEBIAN_FRONTEND=noninteractive

COPY . .

RUN pip install -r requirements/requirement.txt 

WORKDIR src

CMD ["sh", "-c", "python main.py"]