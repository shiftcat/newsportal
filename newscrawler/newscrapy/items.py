# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RecentItem(scrapy.Item):
    articleId = scrapy.Field()
    press = scrapy.Field()
    link = scrapy.Field()
    subject = scrapy.Field()
    summary = scrapy.Field()
    repoter = scrapy.Field()
    date = scrapy.Field()
    thumb = scrapy.Field()



class ArticleItem(scrapy.Item):
    articleId = scrapy.Field()
    press = scrapy.Field()
    url = scrapy.Field()
    subject = scrapy.Field()
    content = scrapy.Field()
    images = scrapy.Field()
    repoter = scrapy.Field()
    wordcount = scrapy.Field()
    date = scrapy.Field()