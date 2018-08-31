FROM ubuntu:16.04

ENV LANG=C.UTF-8

RUN apt-get -y update
RUN apt-get install -y software-properties-common vim unzip curl

# Java 설치
RUN \
  echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections && \
  add-apt-repository -y ppa:webupd8team/java && \
  apt-get update && \
  apt-get install -y oracle-java8-installer && \
  rm -rf /var/lib/apt/lists/* && \
  rm -rf /var/cache/oracle-jdk8-installer

# Define commonly used JAVA_HOME variable
ENV JAVA_HOME /usr/lib/jvm/java-8-oracle
ENV CLASSPATH .:${CLASSPATH}
ENV PATH ${JAVA_HOME}/bin:${PATH}

# 임시 디렉토리 생성
RUN mkdir /download
WORKDIR /download

# 설치 파일 다운로드 및 설치
RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.1.1.zip
RUN wget https://oss.sonatype.org/service/local/repositories/releases/content/org/bitbucket/eunjeon/elasticsearch-analysis-seunjeon/6.1.1.1/elasticsearch-analysis-seunjeon-6.1.1.1.zip
RUN unzip elasticsearch-6.1.1.zip -d /
RUN mv /elasticsearch-6.1.1 /elas
WORKDIR /elas

# 한글 형태소 플러그인 설치
RUN /elas/bin/elasticsearch-plugin install file:///download/elasticsearch-analysis-seunjeon-6.1.1.1.zip
RUN rm -rf /download

VOLUME ["/elas/data", "/elas/logs"]

# 리눅스 사용자 추가
# RUN groupadd -g 1000 elasticsearch && useradd elasticsearch -u 1000 -g 1000
RUN \
  groupadd -g 1000 elasticsearch && \
  useradd -ms /bin/bash -u 1000 -g 1000 elasticsearch 
# 도커 기동 후 볼륨으로 지정한 디렉토리가 root소유자로 바뀜... ㅠ
# RUN chown elasticsearch:elasticsearch -R /elas
# USER elasticsearch
WORKDIR /elas

ADD index.json /elas/index.json

# 네트워크 설정
RUN \
  echo "network.host: 0.0.0.0" > /elas/config/elasticsearch.yml && \
  echo "http.port: 9200" >> /elas/config/elasticsearch.yml


# 실행 쉘 스크립트 생성
RUN \
  echo "#!/bin/bash" >> start.sh && \
  echo "chown elasticsearch:elasticsearch -R /elas" >> start.sh && \
  echo "su - elasticsearch -c /elas/bin/elasticsearch >& /dev/null &" >> start.sh && \
  echo "sleep 15" >> start.sh && \
  echo "curl -s -H \"Content-Type: application/json\" -XPUT http://localhost:9200/news?pretty -d @/elas/index.json" >> start.sh && \
  echo "tail -f /elas/logs/elasticsearch.log" >> start.sh


RUN chmod 755 start.sh

EXPOSE 9200
EXPOSE 9300

CMD /elas/start.sh
#CMD /bin/bash
