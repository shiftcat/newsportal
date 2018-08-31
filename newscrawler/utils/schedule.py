

from datetime import datetime
from utils.mongo import MongDAO
from newscrapy import settings

class Scheduling():
    """
    스케줄러의 시작 종료 일시 및 처리결과를 몽고디비에 기록한다.

    Attributes:
        collection_nm: 스케줄 처리 상태를 저장할 컬렉션
        name: 스케줄러의 이름
        mongodao: 몽고디비 데이터 엑세스 오브젝트
   """

    def __init__(self, name):
        self.collection_nm = 'schedule'
        self.name = name
        self.mongodao = MongDAO(settings)


    def begin(self):
        crawl = {
            'name': self.name,
            'start': datetime.now(),
            'end': None,
            'status': None
        }
        row = self.mongodao.insert(self.collection_nm, crawl)
        return row.inserted_id


    def end(self, inserted_id, status):
        shced = self.mongodao.find_one(self.collection_nm, {'_id': inserted_id})
        shced['end'] = datetime.now()
        shced['status'] = status
        self.mongodao.update(self.collection_nm, shced)
