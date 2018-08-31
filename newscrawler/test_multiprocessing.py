

from scrapy import cmdline
from scrapy.crawler import CrawlerRunner
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from newscrapy.spiders.new_article import ArticleSpider

from multiprocessing import Process

def crawl_article_pro():
    process = CrawlerProcess(get_project_settings())
    process.crawl(ArticleSpider)
    process.start()


from twisted.internet import reactor

def crawl_article_run():
    process = CrawlerRunner(get_project_settings())
    deferred = process.crawl(ArticleSpider)
    deferred.addCallback(reactor.callLater, 5, crawl_article_run)
    return deferred


def crawl_article_process():
    p = Process(target=crawl_article_pro, name="crawl_article")
    p.start()
    p.join()


def run_spider_cmd():
    print("Running spider")
    cmdline.execute("scrapy crawl newrecent".split())

crawl_article_process()