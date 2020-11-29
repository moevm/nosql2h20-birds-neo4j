FROM ubuntu:20.04

MAINTAINER jozo <hi@jozo.io>

WORKDIR /birdwather_app
# Add user
RUN adduser --quiet --disabled-password qtuser

COPY src src
COPY res res

RUN apt-get update
# 'noninteractive' prevents a stupid dialog when tzdata is being installed
RUN DEBIAN_FRONTEND="noninteractive" apt-get install tzdata
# installing python3-pyqt5 instead of python3 prevents us from manually installing lots of related libs
RUN apt-get install  -y python3-pyqt5 python3-pip
RUN pip3 install PyQt5 PyQtWebEngine matplotlib neo4j
RUN apt-get install -y libnss3
RUN apt-get install -y libasound2-dev
RUN pip3 install idna
# export needed cuz import is gonna search for modules in /src/ otherwise
#RUN export PYTHONPATH=/app
#RUN export PATH=/app
#RUN export PYTHONUNBUFFERED=1

#EXPOSE 7687
