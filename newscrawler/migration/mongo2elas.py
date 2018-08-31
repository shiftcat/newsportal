
"""

이 모듈은 몽고디비에서 엘라스티서치로 데이터를 이관하는 모듈이다.

이 기능은 로그스테시를 이용하여 처리할 수 있다.

"""
import pymongo
from elasticsearch import Elasticsearch

from newscrapy import settings
from utils.schedule import Scheduling
from utils.logger import get_logger
from utils.mongo import MongDAO


es = Elasticsearch(host=settings.ELASTIC_SERVER, port=settings.ELASTIC_PORT, timeout=60)

logger = get_logger('mig')

mongdao = MongDAO(settings)


def entries_to_remove(entries, the_dict):
    for key in entries:
        if key in the_dict:
            del the_dict[key]


def all_unset():
    mongdao.update_many('articles', {}, {"$set": {"elas": 0}})


cond = {
    '$or': [
        {'elas': None},
        {'elas': {'$exists': False}},
        {'elas': 0}
    ]
}


def get_articles_count():
    return mongdao.count('articles', cond)


def get_articles():
    return mongdao.find('articles', cond, sort=[('date', pymongo.ASCENDING)], limit=50)


def replace_article(row):
    mongdao.update('articles', row)


def save_to_elas(row):
    success = 0
    fail = 0
    tr = row.copy()
    entries_to_remove(['_id', 'ins_dt', 'upd_dt'], tr)
    try:
        es.index(index="news", doc_type="article", id=row['articleId'], body=tr)
    except Exception as error:
        logger.error(error)
        fail = 1
        row['elas'] = -1
        replace_article(row)
    else:
        success = 1
        row['elas'] = 1
        replace_article(row)
        logger.debug("{} elasticsearch save complete!".format(row['articleId']))
    return success, fail


def mingrate():
    logger.debug("=== mingrate begin ====")
    scheduling = Scheduling("mig")
    mid = scheduling.begin()
    success_cnt = 0
    fail_cnt = 0
    while True:
        cnt = get_articles_count()
        if cnt > 0:
            rows = get_articles()
            for row in rows:
                logger.debug("{} migration begin".format(row['articleId']))
                success, file = save_to_elas(row)
                success_cnt += success
                fail_cnt += file
        else:
            break
    scheduling.end(mid, {'success_count': success_cnt, 'fail_count': fail_cnt})
    logger.debug("=== mingrate end ====")


if __name__ == "__main__":
    mingrate()