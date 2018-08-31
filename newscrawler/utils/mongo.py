
import pymongo

from utils.logger import get_logger


logger = get_logger(__name__)


def mong_conn(func):
    def wrapper(*args, **kwargs):
        settings = args[0].settings
        conn = pymongo.MongoClient(settings.MONGODB_SERVER, settings.MONGODB_PORT)
        db = conn.news
        args[0].db = db
        try:
            res = func(*args, **kwargs)
        finally:
            conn.close()
            del args[0].db
        return res

    return wrapper



class MongDAO():

    def __init__(self, settings):
        self.settings = settings


    def _get_collection(self, coll):
        try:
            collection = self.db[coll]
        except:
            self.db.create_collection(coll)
            collection = self.db[coll]
        logger.debug("get collection ==> {}".format(collection))
        return collection


    @mong_conn
    def count(self, coll, cond={}):
        collection = self._get_collection(coll)
        cnt = collection.find(cond).count()
        logger.debug("count ==> {}: {}".format(coll, str(cnt)))
        return cnt

    @mong_conn
    def find(self, coll, cond={}, sort=None, limit=None):
        collection = self._get_collection(coll)
        obj = collection.find(cond)
        if sort is not None:
            obj = obj.sort(sort)
        if limit is not None:
            obj = obj.limit(limit)
        logger.debug("find {}: {} | {} | {}".format(coll, cond, sort, str(limit)))
        return obj

    @mong_conn
    def find_one(self, coll, cond):
        collection = self._get_collection(coll)
        row = collection.find_one(cond)
        logger.debug("find_one {}: {}".format(coll, row))
        return row

    @mong_conn
    def insert(self, coll, doc):
        collection = self._get_collection(coll)
        res = collection.insert_one(doc)
        logger.debug("insert {}: {}".format(coll, res))
        return res


    @mong_conn
    def update(self, coll, doc):
        collection = self._get_collection(coll)
        res = collection.replace_one({'_id': doc['_id']}, doc)
        logger.debug("update {}: {}".format(coll, res))
        return res


    @mong_conn
    def update_many(self, coll, cond, val):
        collection = self._get_collection(coll)
        res = collection.update_many(cond, val)
        logger.debug("update_many {}: {}".format(coll, res))
        return res


    @mong_conn
    def delete(self, coll, id):
        collection = self._get_collection(coll)
        res = collection.remove({'_id': id})
        logger.debug("delete {}: {}".format(coll, res))
        return res



if __name__ == "__main__":

    class settings():
        MONGODB_SERVER = "localhost"
        MONGODB_PORT = 27017


    dao = MongDAO(settings)
    cnt = dao.count('articles')
    print(cnt)
    res = dao.find('articles', {}, sort=[('date', pymongo.DESCENDING)], limit=10)
    for r in res:
        if r.get('summary') is not None:
            print(r)
            # dao.delete('articles', r['_id'])