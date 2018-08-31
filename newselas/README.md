
**다음과 같은 오류가 발생 한다면**
```
[1] bootstrap checks failed
[1]: max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
```
**도커가 설치된 컴에서 다음 명령어를 실행한다.**
```
sudo sysctl -w vm.max_map_count=262144
```


### Docker RUN
```
docker build -t elasticsearch:6.1.1 .

docker run -it -p 9200:9200 --rm -v /mnt/data/dbdata/elas/data:/elas/data --name elasticsearch elasticsearch:6.1.1
```


### 인덱스 삭제
```
curl -s -XDELETE http://localhost:9200/news
```
### 인덱스 생성
```
curl -s -H "Content-Type: application/json" -XPUT http://localhost:9200/news?pretty -d @index.json
```

### 인덱스 조회
```
curl -s -XGET http://localhost:9200/news?pretty
or
curl -s -XGET http://localhost:9200/news/article/_mapping?pretty
```
