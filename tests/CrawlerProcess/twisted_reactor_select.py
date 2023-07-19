import frapy
from frapy.crawler import CrawlerProcess


class SelectReactorSpider(frapy.Spider):
    name = "epoll_reactor"


process = CrawlerProcess(
    settings={
        "TWISTED_REACTOR": "twisted.internet.selectreactor.SelectReactor",
    }
)
process.crawl(SelectReactorSpider)
process.start()
