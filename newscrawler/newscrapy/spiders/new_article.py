# -*- coding: utf-8 -*-


import scrapy
import pymongo
from newscrapy.spiders.parser.khan_parser import KhanItemParser
from newscrapy.spiders.parser.khan_parser import BizKhanItemParser
from newscrapy.spiders.parser.chosun_parser import ChosunArticleParser
from newscrapy import settings

from urllib.parse import urlparse
from utils.mongo import MongDAO

mongodao = MongDAO(settings)

class ArticleSpider(scrapy.Spider):

    name = 'newarticle'

    allowed_domains = ['news.khan.co.kr', 'news.chosun.com']

    custom_settings = {
        'ITEM_PIPELINES' : {
            'newscrapy.pipelines.ArticlePipeline': 100,
        }
    }


    # def __cond(self):
    #     cond = {
    #         '$and': [
    #             {'press': 'CHO'},
    #             {
    #                 '$or': [
    #                     # {'crawl': {'$ne': None}},
    #                     {'crawl': None},
    #                     {'crawl': {'$exists': False}}
    #                 ]
    #             }
    #         ]
    #     }
    #     return cond


    def __cond(self):
        cond = {
            '$or': [
                # {'crawl': {'$ne': None}},
                {'crawl': None},
                {'crawl': {'$exists': False}}
            ]
        }
        return cond


    def start_requests(self):
        requests = mongodao.find('recents', self.__cond(), sort=[('date', pymongo.DESCENDING)], limit=20)
        for req in requests:
            link = req.get('link')
            if link:
                call_back = self.parse_index_warp(req)
                yield scrapy.Request(link, call_back)



    def parse_index_warp(self, recent):

        def parse_index(response):
            self.logger.debug(response.url)
            self.logger.debug("파서 시작 ====>")
            url = urlparse(response.url)

            article = {}
            if url.netloc == 'news.khan.co.kr':
                parser = KhanItemParser()
                article = parser.make_item(response)
            elif url.netloc == 'biz.khan.co.kr':
                parser = BizKhanItemParser()
                article = parser.make_item(response)
            elif url.netloc == 'news.chosun.com':
                parser = ChosunArticleParser()
                article = parser.make_item(response)

            article['press'] = recent['press']
            article['articleId'] = recent['articleId']
            article['url'] = response.url
            self.logger.debug(article)

            self.logger.debug("파서 종료 ====>")

            return article

        return parse_index