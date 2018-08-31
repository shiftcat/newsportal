# -*- coding: utf-8 -*-

from abc import abstractmethod
from newscrapy.items import ArticleItem
from newscrapy.items import RecentItem

import logging



class RecentParser(object):

    def __init__(self, press_code):
        self.__press = press_code
        self.logger = logging.getLogger()
        pass


    def make_item(self, item):
        recentItem = RecentItem()
        recentItem['press'] = self.__press
        recentItem['articleId'] = self.__press + self.get_article_id(item)
        recentItem['link'] = self.get_link(item)
        recentItem['subject'] = self.get_subject(item)
        recentItem['summary'] = self.get_summary(item)
        recentItem['repoter'] = self.get_repoter(item)
        recentItem['date'] = self.get_date(item)
        recentItem['thumb'] = self.get_thumb(item)
        return recentItem


    @abstractmethod
    def get_article_id(self, item):
        pass


    @abstractmethod
    def get_link(self, item):
        pass


    @abstractmethod
    def get_subject(self, item):
        pass


    @abstractmethod
    def get_summary(self, item):
        pass


    @abstractmethod
    def get_repoter(self, item):
        pass


    @abstractmethod
    def get_date(self, item):
        pass


    @abstractmethod
    def get_thumb(self, item):
        pass



class ArticleParser(object):

    def __init__(self):
        self.logger = logging.getLogger()


    def make_item(self, body):
        articleItem = ArticleItem()
        articleItem['subject'] = self.get_subject(body)
        articleItem['content'] = self.get_content(body)
        articleItem['images'] = self.get_images(body)
        articleItem['repoter'] = self.get_repoter(body)
        articleItem['date'] = self.get_date(body)
        return articleItem


    @abstractmethod
    def get_subject(self, body):
        pass


    @abstractmethod
    def get_content(self, body):
        pass


    @abstractmethod
    def get_images(self, body):
        pass


    @abstractmethod
    def get_repoter(self, body):
        pass


    @abstractmethod
    def get_date(self, body):
        pass