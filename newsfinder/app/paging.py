
import math
import logging


class PageValue():


    def __init__(self, url, start_row):
        self.start_row = start_row
        self.url = url
        pass


    def _page(self, start, end, current):
        self.start_pg = start
        self.end_pg = end
        self.current_page = current


    def _page_group(self, total, current):
        self.total_group = total
        self.current_group = current


    def getPages(self):
        pages = []
        for pn in range(self.start_pg, self.end_pg+1):
            pages.append( {'url': "{}{}".format(self.url, pn), 'page_num': pn} )
        return pages


    def getStartRow(self):
        return self.start_row


    def getPrev(self):
        if self.current_group > 0:
            return "{}{}".format(self.url, self.start_pg-1)


    def getNext(self):
        if self.current_group < (self.total_group-1):
            return "{}{}".format(self.url, self.end_pg+1)


    def getCurrentPage(self):
        return self.current_page



class Page():

    def __init__(self, rows_per_page=15, pgnum_per_page=5):
        self.logger = logging
        self.rows_per_page = rows_per_page
        self.pgnum_per_page = pgnum_per_page
        pass


    def paging(self, url, total_cnt, curr_page):

        if total_cnt < 0:
            raise Exception("total_cnt less than 0")

        if curr_page < 1:
            raise Exception("curr_page less than 1")

        tot_page = math.ceil(total_cnt / self.rows_per_page)
        curr_page = curr_page > tot_page and tot_page or curr_page

        tot_group = math.ceil(tot_page / self.pgnum_per_page)
        # 0 에서 시작
        curr_group = int((curr_page-1) / self.pgnum_per_page)

        start_pg = (curr_group * self.pgnum_per_page) + 1
        end_pg = (curr_group+1) * self.pgnum_per_page

        if end_pg > tot_page:
            end_pg = tot_page

        # print(end_pg, " ", tot_page, " ", end_pg > tot_page)
        # end_pg = (end_pg > tot_page) and tot_page or end_pg

        start_row = (curr_page-1) * self.rows_per_page

        self.logger.debug("tot_page => {}".format(tot_page))
        self.logger.debug("tot_group => {}".format(tot_group))
        self.logger.debug("curr_group => {}".format(curr_group))
        self.logger.debug("start_pg => {}".format(start_pg))
        self.logger.debug("end_pg => {}".format(end_pg))

        pageValue = PageValue(url, start_row)
        pageValue._page(start_pg, end_pg, curr_page)
        pageValue._page_group(tot_group, curr_group)
        return pageValue



if __name__ == "__main__":
    p = Page(10, 10)
    pages = p.paging("myurl?page=", 280, 30)

    print("start_row", pages.getStartRow())

    if pages.getPrev():
        print("prev => ", pages.getPrev())

    for pg in pages.getPages():
        print(pg['url'], " ", pg['page_num'])

    if pages.getNext():
        print("next => ", pages.getNext())