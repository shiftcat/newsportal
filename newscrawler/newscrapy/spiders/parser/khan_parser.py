# -*- coding: utf-8 -*-

from newscrapy.spiders.parser import ArticleParser
from newscrapy.spiders.parser import RecentParser

from urllib.parse import urlsplit, parse_qs



class KahnRecentParser(RecentParser):

    # def __init__(self, press_code):
    #     super(press_code)

    def get_byline(self, item):
        return item.xpath('span[@class="byline"]/em')


    # def get_em_data(self, item, idx):
    #     byline = self.get_byline(item)



    def get_date(self, item):
        ems = self.get_byline(item)
        self.logger.debug(ems)

        s = ''
        if len(ems) < 3:
            s = ems[1].xpath('text()').extract()
        elif len(ems) < 4:
            s = ems[2].xpath('text()').extract()
        self.logger.debug(s)
        if type(s) == list:
            s = s[0]
        sl = s.split()
        dsl = sl[:-1]
        ds = ''.join(dsl).strip()
        dts = ' '.join([ds, sl[-1]])
        # dt = datetime.strptime(dts, '%Y.%m.%d %H:%M')
        return dts


    def get_article_id(self, item):
        link = self.get_link(item)
        query = urlsplit(link).query
        params = parse_qs(query)
        return params['artid'][0]


    def get_link(self, item):
        lns = item.xpath('strong/a/@href').extract()
        if type(lns) == str:
            return lns
        elif type(lns) == list:
            return lns[0]


    def get_subject(self, item):
        sl = item.xpath('strong/a/text()').extract()
        if type(sl) == list:
            return sl[0]
        else:
            return sl


    def get_summary(self, item):
        s = item.xpath('span[@class="lead"]/text()').extract()
        s = ' '.join(s)
        return s.replace('\n', '').replace('\r', '').strip()


    def get_repoter(self, item):
        ems = self.get_byline(item)
        self.logger.debug(ems)

        s = ''
        if len(ems) > 2:
            s = ems[1].xpath('text()').extract()
        self.logger.debug(s)

        if s:
            s = ' '.join(s)
            return s.replace('기자', '').strip()
        else:
            return ''


    def get_thumb(self, item):
        return None



class KhanItemParser(ArticleParser):

    def get_subject(self, body):
        subject = body.xpath(".//div[contains(@class, 'art_header')]/div[@class='subject']/h1/text()").extract_first()
        return subject.strip()


    def get_repoter(self, body):
        repoter = body.xpath(".//div[contains(@class, 'art_header')]/div[@class='subject']/span/a/text()").extract_first()
        if repoter:
            return repoter.strip()
        else:
            return ''


    def get_content(self, body):
        chungk_tags = body.xpath(".//div[@class='art_body']/p[@class='content_text']")
        contents_list = []
        for chungk in chungk_tags:
            chs = chungk.xpath('text()').extract_first()
            if chs:
                contents_list.append(chs)
        return ' '.join(contents_list)


    def get_images(self, body):
        img_list = []
        for img_contain in body.xpath(".//div[contains(@class, 'art_photo photo_center')]"):
            src = img_contain.xpath("div[@class='art_photo_wrap']/img/@src").extract_first()
            alt = img_contain.xpath("div[@class='art_photo_wrap']/img/@alt").extract_first()
            if src:
                img_map = {}
                img_map['src'] = src
                img_map['alt'] = alt
                img_list.append(img_map)
        self.logger.debug(img_list)
        return img_list


    # def list_to_string(self, slist, d=''):
    #     if type(slist) == list:
    #         return d.join(slist).strip()
    #     else:
    #         return slist


    def get_date(self, body):
        date = {}
        emtags = body.xpath(".//div[contains(@class, 'art_header')]/div[@class='function_wrap']/div[@class='pagecontrol']/div[@class='byline']")
        # emtags = body.xpath("//*[@id='container']/div[1]/div[2]/div[2]/div/em").extract()
        self.logger.debug(emtags[0])
        if len(emtags) > 0:
            first_ins = body.xpath(".//div[contains(@class, 'art_header')]/div[@class='function_wrap']/div[@class='pagecontrol']/div[@class='byline']/em[1]/text()").extract_first()
            _arr = first_ins.split(' ')
            first_ins = ' '.join([_arr[-2], _arr[-1]])
            date['first_ins'] = first_ins
        if len(emtags) > 1:
            # last_upd = body.xpath(".//div[contains(@class, 'art_header')]/div[@class='function_wrap']/div[@class='pagecontrol']/div[@class='byline']/em[2]/text()").extract_first()
            last_upd = emtags[1].xpath('text()').extract_first()
            _arr = last_upd.split(' ')
            last_upd = ' '.join([_arr[-2], _arr[-1]])
            date['last_upd'] = last_upd
        self.logger.debug(date)
        return date




class BizKhanItemParser(ArticleParser):
    def get_subject(self, body):
        subject = body.xpath('.//*[@id="articleTtitle"]/text()').extract_first()
        return subject.strip()


    def get_repoter(self, body):
        repoter = body.xpath('//*[@id="container"]/div[2]/div[1]/div[1]/span/a/text()').extract_first()
        if repoter:
            return repoter.strip()
        else:
            return ''


    def get_content(self, body):
        chungk_tags = body.xpath('//*[@id="container"]/div[2]/div[2]/div[1]/p')
        contents_list = []
        for chungk in chungk_tags:
            chs = chungk.xpath('text()').extract_first()
            if chs:
                contents_list.append(chs)
        return ' '.join(contents_list)


    def get_images(self, body):
        img_list = []
        for img_contain in body.xpath(".//div[contains(@class, 'art_photo photo_center')]"):
            src = img_contain.xpath("div[@class='art_photo_wrap']/img/@src").extract_first()
            alt = img_contain.xpath("div[@class='art_photo_wrap']/img/@alt").extract_first()
            if src:
                img_map = {}
                img_map['src'] = src
                img_map['alt'] = alt
                img_list.append(img_map)
        self.logger.debug(img_list)
        return img_list


    # def list_to_string(self, slist, d=''):
    #     if type(slist) == list:
    #         return d.join(slist).strip()
    #     else:
    #         return slist


    def get_date(self, body):
        date = {}
        emtags = body.xpath('//*[@id="bylineArea"]')
        # emtags = body.xpath("//*[@id='container']/div[1]/div[2]/div[2]/div/em").extract()
        self.logger.debug(emtags[0])
        if len(emtags) > 0:
            first_ins = body.xpath('//*[@id="bylineArea"]/em[1]/text()').extract_first()
            _arr = first_ins.split(' ')
            first_ins = ' '.join([_arr[-2], _arr[-1]])
            date['first_ins'] = first_ins
        if len(emtags) > 1:
            last_upd = body.xpath('//*[@id="bylineArea"]/em[2]/text()').extract_first()
            _arr = last_upd.split(' ')
            last_upd = ' '.join([_arr[-2], _arr[-1]])
            date['last_upd'] = last_upd
        self.logger.debug(date)
        return date