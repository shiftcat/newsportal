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


## docker-compose
```
docker-compose up --build

docker ps

docker stats

docker-compose down
```