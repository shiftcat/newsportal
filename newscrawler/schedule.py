

import time

from multiprocessing import Process

import subprocess
from subprocess import Popen

from apscheduler.schedulers.background import BackgroundScheduler


from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from newscrapy.spiders.news_recent import RecentArtSpider
from newscrapy.spiders.new_article import ArticleSpider

from migration.mongo2elas import mingrate


# ===================================================
# 파이썬 코드로 크롤러를 APSchedule에 의해 실행할 경우 교착상태 빠지는 경우가 발생한다.
# utex(0x7f58a31999d0, FUTEX_WAIT, ...
# ===================================================
def crawl_recent():
    process = CrawlerProcess(get_project_settings())
    process.crawl(RecentArtSpider)
    process.start()


def crawl_recent_process():
    p = Process(target=crawl_recent, name="crawl_recent")
    p.start()
    p.join()



def crawl_article():
    process = CrawlerProcess(get_project_settings())
    process.crawl(ArticleSpider)
    process.start()


def crawl_article_process():
    p = Process(target=crawl_article, name="crawl_article")
    p.start()
    p.join()


def mingrate_process():
    p = Process(target=mingrate, name="mingrate")
    p.start()
    p.join()


# ================================================
# 위와 같은 문제로 subprocess.Poepn()을 사용하여 실행 되도록 하였다.
# ================================================
def popen_recent_scrapy():
    with Popen(["scrapy", "crawl", "newrecent"], stdout=subprocess.PIPE) as proc:
        proc.communicate()


def popen_article_scrapy():
    with Popen(["scrapy", "crawl", "newarticle"], stdout=subprocess.PIPE) as proc:
        proc.communicate()


def popen_migrate():
    with Popen(["python3.6", "mig.py"], stdout=subprocess.PIPE) as proc:
        proc.communicate()


def schedule():
    sched = BackgroundScheduler()
    sched.start()

    # "cron => hour="", minute="", second=""
    # "interval" => hours=, minutes=, seconds=
    sched.add_job(popen_recent_scrapy, 'cron',   hour="*/1", id="crawl_recent")
    sched.add_job(popen_article_scrapy, 'cron', minute="*/20", id="crawl_article")
    sched.add_job(popen_migrate, 'cron', minute="*/30", id="mingrate")

    while True:
        time.sleep(1)



import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)


if __name__ == "__main__":
    schedule()