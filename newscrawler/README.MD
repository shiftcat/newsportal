
# newscrawler

이 프로젝트는 언론사 사이트에서 뉴스 기사을 크롤링하는 프로젝트이다.

최신 기사 목록을 크롤링한 후 이 목록으로 부터 해당 기사를 크롤링하는 방식으로 진행된다.

따라서 크롤러는 다음 2가지로 구성되어 있다.

* 최신 기사 목록 크롤러
* 기사 본문 크롤러

**2018-08 현재 정상적으로 크롤링 됨을 확인 하였지만 해당 사이트의 변경으로 정상적으로 크롤링 되지 않을 수도 있다.**

#### 프로젝트 환경
* Scrapy 1.5.1
* MongoDB 4.0.1
* APScheduler 3.5.2


### MongoDB
news database에 다음 collection에 크롤링 데이터를 저장한다.
* recents : 최신 기사 목록 데이터
* articles: 기사 본문 데이터
* schedule: 스케줄링 데이터


# 크롤러 실행

크롤러를 실행하는 방법은 3가지가 있다.
* 크롤러 단독 실행
* 스케줄러에 의한 실행
* scrapyd에 의한 실행


## scrapy 단독 실행
```commandline

$ scrapy crawl newrecent

$ scrapy crawl newarticle

```


## APScheduler에 의한 실행 
schedule.py에 스케줄링이 작성되어 있다.

```commandline

$ python schedule.py

```


## scrapyd를 이용한 크롤링 실행

### scrapyd 설치

설치 후 scrapyd 명령어로 서버를 실행 한다.

```commandline

$ pip install scrapyd
$ pip install scrapyd-client
$ scrapyd

```

### scrapyd에 배포

scrapy.cfg 파일이 있는 프로젝트 디렉토리에서 scrapyd-deploy 명어로 배포 한다.

성공적으로 배포가 되면 브라우저를 열어 프로젝트 배포상태를 확인 한다.

http://localhost:6800/

```commandline

$ scrapyd-deploy

```



### 크롤링 시작

```commandline

curl http://localhost:6800/schedule.json -d project=newscrapy -d spider=newrecent

curl http://localhost:6800/schedule.json -d project=newscrapy -d spider=newarticle

```

### 크롤러 제거
```commandline

curl http://localhost:6800/delproject.json -d project=newscrapy

```

## Docker run

```commandline

docker run --rm --name mongodb -p 27027:27017 -v /mnt/data/dbdata/mongo:/data/db -d mongo

docker build -t newscrawler:latest .

docker run -it --rm --name newscrawler --link mongodb:mongodb --link elasticsearch newscrawler:latest

# 최신 기사 목록 크롤링은 처음 한 번은 수동으로 실행한다.
docker exec -t newscrawler scrapy crawl newrecent

```