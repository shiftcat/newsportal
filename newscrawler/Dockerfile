FROM ubuntu:16.04
RUN apt-get -y update

RUN apt-get install -y software-properties-common

# Java 설치
# Java가 필요한 이유는 파이썬 모둘 중 JPype1 모듈이 자바를 필요로 한다.
# JPype1는 konlpy 와 함께 한글 형태소 분석에 사용되는 라이브러리 이다.
RUN \
  echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections && \
  add-apt-repository -y ppa:webupd8team/java && \
  apt-get update && \
  apt-get install -y oracle-java8-installer && \
  rm -rf /var/lib/apt/lists/* && \
  rm -rf /var/cache/oracle-jdk8-installer


# Define commonly used JAVA_HOME variable
ENV JAVA_HOME /usr/lib/jvm/java-8-oracle

# 파이선 3.6 설치
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y --no-install-recommends build-essential python3.6 python3.6-dev python3-pip python3-setuptools
RUN apt-get install -y git

RUN python3.6 -m pip install pip --upgrade

ENV LANG=C.UTF-8

ADD . /newscrawler

WORKDIR /newscrawler

RUN pip3.6 install -r requirements.txt


CMD python3.6 schedule.py