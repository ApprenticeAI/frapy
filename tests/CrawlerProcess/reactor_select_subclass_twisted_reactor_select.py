from twisted.internet.main import installReactor
from twisted.internet.selectreactor import SelectReactor

import frapy
from frapy.crawler import CrawlerProcess


class SelectReactorSubclass(SelectReactor):
    pass


reactor = SelectReactorSubclass()
installReactor(reactor)


class NoRequestsSpider(frapy.Spider):
    name = "no_request"

    def start_requests(self):
        return []


process = CrawlerProcess(
    settings={
        "TWISTED_REACTOR": "twisted.internet.selectreactor.SelectReactor",
    }
)

process.crawl(NoRequestsSpider)
process.start()
