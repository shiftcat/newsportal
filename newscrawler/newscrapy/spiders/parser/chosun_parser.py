# -*- coding: utf-8 -*-


from newscrapy.spiders.parser import ArticleParser
from newscrapy.spiders.parser import RecentParser

from urllib.parse import urlsplit

import re

class ChosunRecentParser(RecentParser):


    def get_date(self, item):
        s = item.xpath('dd[@class="date_author"]/span[@class="date"]/text()').extract_first()
        return s


    def get_article_id(self, item):
        link = self.get_link(item)
        path = urlsplit(link).path
        arr_path = path.split('/')
        end_path = arr_path[-1]
        arr_end = end_path.split('.')
        return arr_end[0]


    def get_link(self, item):
        lns = item.xpath('dt/a//@href').extract_first()
        return lns


    def get_subject(self, item):
        sl = item.xpath('dt/a/text()').extract_first()
        return sl


    def get_summary(self, item):
        s = item.xpath('dd[@class="desc"]/a/text()').extract_first()
        if s:
            return s.replace('\n', '').replace('\r', '').strip()
        else:
            return ''


    def get_repoter(self, item):
        s = item.xpath('dd[@class="date_author"]/span[@class="author"]/a/text()').extract_first()
        return s


    def get_thumb(self, item):
        s = item.xpath('dd[@class="thumb"]/a/img/@src').extract_first()
        return s






class ChosunArticleParser(ArticleParser):


    def get_subject(self, body):
        subject = body.xpath('//*[@id="news_title_text_id"]/text()').extract_first()
        return subject.strip()


    def get_repoter(self, body):
        repoter = body.xpath('.//div[@class="news_title_author"]/li[@id="j1"]/a/text()').extract_first()
        if repoter:
            return repoter.strip()
        else:
            return ''


    def get_content(self, body):
        chungk_tags = body.xpath('//*[@id="news_body_id"]/div[@class="par"]')
        contents_list = []

        for chungk in chungk_tags:
            ptag = chungk.xpath('p')
            if (len(ptag)) > 0:
                for p in chungk.xpath('p/text()').extract():
                    contents_list.append(p)
            else:
                for p in chungk.xpath('text()').extract():
                    contents_list.append(p)

        s = ' '.join(contents_list).replace('\n', ' ').replace('\r', ' ')
        return s


    def get_images(self, body):
        img_list = []
        for img_contain in body.xpath('//*[@id="news_body_id"]/div[contains(@class, "news_imgbox")]'):
            src = img_contain.xpath("figure/img/@src").extract_first()
            alt = img_contain.xpath("figure/img/@alt").extract_first()
            if src:
                img_map = {}
                img_map['src'] = src
                img_map['alt'] = alt
                img_list.append(img_map)
        self.logger.debug(img_list)
        return img_list



    def list_to_string(self, slist, d=''):
        if type(slist) == list:
            return d.join(slist).strip()
        else:
            return slist



    # """
    # 입력 2018.08.16 03:31 | 수정 2018.08.16 03:34
    # """
    def get_date(self, body):
        date = {}
        dates = body.xpath('.//div[@class="news_date"]/text()').extract_first()
        arr_date = dates.split('|')
        if len(arr_date) > 0:
            first_ins = arr_date[0].replace('입력', '').strip()
            date['first_ins'] = first_ins + ':00'
        if len(arr_date) > 1:
            last_upd = arr_date[1].replace('수정', '').strip()
            date['last_upd'] = last_upd + ':00'
        self.logger.debug(dates)
        return date