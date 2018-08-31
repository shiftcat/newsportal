

from datetime import datetime
from pymongo import MongoClient

from newscrapy import settings


class CrawlLogger():

    def __init__(self, settings, name):
        self.collection_nm = 'crawl'
        self.settings = settings
        self.name = name


    def __get_collection(self, db):
        collection = None
        try:
            collection = db[self.collection_nm]
        except:
            db.createCollection(self.collection_nm)
            collection = db[self.collection_nm]
        return collection


    def begin(self):
        with MongoClient(settings.MONGODB_SERVER, settings.MONGODB_PORT) as client:
            db = client[settings.MONGODB_DB_NEWS]
            collection = self.__get_collection(db)

            crawl = {
                'name': self.name,
                'start': datetime.now(),
                'end': None,
                'status': None
            }

            res = collection.insert_one(crawl)
            return res.inserted_id


    def end(self, inserted_id, status):
        with MongoClient(settings.MONGODB_SERVER, settings.MONGODB_PORT) as client:
            db = client[settings.MONGODB_DB_NEWS]
            collection = self.__get_collection(db)

            crawl = collection.find_one({'_id': inserted_id})
            crawl['end'] = datetime.now()
            crawl['status'] = status
            collection.replace_one({'_id': crawl['_id']}, crawl)