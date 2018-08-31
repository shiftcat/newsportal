# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from datetime import datetime

from collections import Counter
from konlpy.tag import Kkma

from utils.schedule import Scheduling
from utils.mongo import MongDAO
from newscrapy import settings





class RecentPipeline(object):

    def open_spider(self, spider):
        self.logger = spider.logger
        self.mongodao = MongDAO(settings)
        self.scheduling = Scheduling(spider.name)
        self.md_id = self.scheduling.begin()


    def close_spider(self, spider):
        self.logger.debug("======== spider close ==========")
        status = spider.crawler.stats.get_stats()
        self.scheduling.end(self.md_id, status)



    def process_item(self, item, spider):
        self.logger.debug('==== recent pipeline start =====')
        row = self.mongodao.find_one('recents', {'articleId': item['articleId']})
        if row:
            row.update(dict(item))
            row['upd_dt'] = datetime.now()
            self.mongodao.update('recents', row)
        else:
            item_map = dict(item)
            item_map['ins_dt'] = datetime.now()
            self.mongodao.insert('recents', item_map)
        return item




def get_tokens(kkma, contect):
    tokens = []
    node = kkma.pos(contect)
    for (taeso, pumsa) in node:
        if pumsa in ('NNG', 'NNP'):
            tokens.append(taeso)
    return tokens


def word_count(content, n):
    tagger = Kkma()
    frequency = Counter()
    tokens = get_tokens(tagger, content)
    frequency.update(tokens)
    rntVal = []
    for token, count in frequency.most_common(n):
        rntVal.append({'word': token, 'count': count})
    return rntVal



class ArticlePipeline(object):

    def open_spider(self, spider):
        self.logger = spider.logger
        self.logger.debug("======== article pipline open ==========")
        self.mongodao = MongDAO(settings)
        self.scheduling = Scheduling(spider.name)
        self.md_id = self.scheduling.begin()


    def close_spider(self, spider):
        self.logger.debug("======== article pipline close ==========")
        status = spider.crawler.stats.get_stats()
        self.scheduling.end(self.md_id, status)


    def update_recent(self, item):
        self.logger.debug('==== recent update start =====')
        n_row = self.mongodao.find_one('recents', {'articleId': item['articleId']})
        if n_row:
            n_row['upd_dt'] = datetime.now()
            n_row['crawl'] = item.get('subject') and 1 or -1
            self.mongodao.update('recents', n_row)
            self.logger.debug('==== update recent item =====')


    def process_item(self, item, spider):
        self.logger.debug('==== article pipeline start =====')
        if item.get('subject'):
            item['wordcount'] = word_count(item['content'], 5)
            a_row = self.mongodao.find_one('articles', {'articleId': item['articleId']})
            if a_row:
                a_row.update(dict(item))
                a_row['upd_dt'] = datetime.now()
                self.mongodao.update('articles', a_row)
            else:
                item_map = dict(item)
                item_map['ins_dt'] = datetime.now()
                self.mongodao.insert('articles', item_map)
        self.update_recent(item)
        self.logger.debug('==== article pipeline end =====')
        return item