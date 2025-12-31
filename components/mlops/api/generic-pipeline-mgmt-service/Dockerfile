# ===============================================================================================================#
# Copyright 2025 Infosys Ltd.                                                                                    #
# Use of this source code is governed by Apache License Version 2.0 that can be found in the LICENSE file or at  #
# http://www.apache.org/licenses/                                                                                #
# ===============================================================================================================#

FROM python:v3.8
ENV DEBIAN_FRONTEND=noninteractive
#RUN apt-get update -y

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

#creating data dir for output
RUN mkdir /data
RUN     chmod 777 /data

RUN mkdir /data/pipeline
RUN     chmod 777 /data/pipeline

RUN mkdir /logs
RUN     chmod 777 /logs

RUN pip install -r requirements.txt  

USER root
WORKDIR $APP_HOME/src

ENTRYPOINT ["python","main.py"]