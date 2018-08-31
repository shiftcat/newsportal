# -*- coding: utf-8 -*-


import scrapy

from newscrapy.spiders.parser.khan_parser import KahnRecentParser
from newscrapy.spiders.parser.chosun_parser import ChosunRecentParser


class RecentArtSpider(scrapy.Spider):

    name = 'newrecent'

    custom_settings = {
        'ITEM_PIPELINES' : {
            'newscrapy.pipelines.RecentPipeline': 100,
        }
    }

    allowed_domains = ['news.khan.co.kr', 'news.chosun.com']

    def start_requests(self):
        for i in range(1, 6):
            yield scrapy.Request("http://news.khan.co.kr/kh_recent/index.html?page={}".format(i), self.khan_parse)

        for i in range(1, 6):
            yield scrapy.Request("http://news.chosun.com/svc/list_in/list.html?source=1&pn={}".format(i),
                                 self.chos_parse)



    def khan_parse(self, response):
        self.logger.debug("KHA 파서 시작 ====>")
        news_list = response.xpath(".//div[@class='news_list']/ul/li")
        recentPars = KahnRecentParser('KHA')
        for item in news_list:
            newItem = recentPars.make_item(item)
            self.logger.debug(newItem.items())
            self.logger.debug("=================")
            yield newItem
        self.logger.debug("KHA 파서 종료 ====>")


    def chos_parse(self, response):
        self.logger.debug("CHO 파서 시작 ====>")
        news_list = response.xpath('//*[@id="list_body_id"]/div[2]/dl')
        recentPars = ChosunRecentParser('CHO')
        for item in news_list:
            newItem = recentPars.make_item(item)
            self.logger.debug(newItem.items())
            self.logger.debug("=================")
            yield newItem
        self.logger.debug("CHO 파서 종료 ====>")