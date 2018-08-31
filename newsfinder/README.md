# newsfinder

이 프로젝트는 엘라스틱 서치를 이용한 뉴스 검색 샘플 프로젝트이다.

메인 페이지는 몽고디비에서 검색은 엘라스틱서치에서 뉴스 기사을 조회하여 그 결과를 웹으로 보여준다.

#### 프로젝트 환경
* Flask
* MongoDB 4.0.1
* Elasticsearch 6.1.1



## Docker run
```commandline

docker build -t newsfinder:latest .

docker run -it --rm -p 8080:8080 --name newsfinder --link mongodb:mongodb --link elasticsearch newsfinder:latest


```