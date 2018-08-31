FROM ubuntu:16.04
RUN apt-get -y update

RUN apt-get install -y software-properties-common

# 파이선 3.6 설치
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y --no-install-recommends build-essential python3.6 python3.6-dev python3-pip python3-setuptools
RUN apt-get install -y git

RUN python3.6 -m pip install pip --upgrade

ENV LANG=C.UTF-8

ADD . /newsfinder

WORKDIR /newsfinder

RUN pip3.6 install -r requirements.txt

EXPOSE 8080

CMD python3.6 main.py