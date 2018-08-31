# NewPortal Project

이 프로젝트는 뉴스 기사의 수집 검색을 위한 샘플 프로젝트이다.

#### 이 프로젝트에는 다음과 같은 하위 프로젝트가 있다.
* newscrawler
    * 뉴스 기사를 수집하기 위한 크롤러가 스케줄러에 의해 동작한다.
* newsfinder 
    * 수집한 뉴스 기사를 보거나 검색할 수 있게 웹으로 제공한다.

#### 프로젝트 환경
* Ubuntu Ubuntu 18.04.1 LTS
* Python 3.6
* Scrapy
* Flask
* MongoDB
* Elasticsearch 6.1.1
* Docker 18.06.1-ce


## .env

docker-compose.yml 파일에서 패스워드와 같이 민감한 내용 또는 환경에 따라 바뀔수 있는 내용은 별도의 파일에 기술한다.

docker-compose.yml과 동일한 경로에 .env파일을 생성한 후 gitignore에 등록하여 git에 공개되지 않도록 한다.

이 프로젝트에서는 .env에 다음 내용이 필요하다.

```
# 몽고디비 데이터 로컬 저장 경로
MONGODB_DATA_PATH=/your path

# 엘라스틱서치 데이터 로컬 저장 경로
ELASTICSEARCH_DATA_PATH=/your path
```


## docker-compose
```
docker-compose up --build

docker ps

docker stats

docker-compose down
```