from twisted.internet import selectreactor

import frapy
from frapy.crawler import CrawlerProcess

selectreactor.install()


class NoRequestsSpider(frapy.Spider):
    name = "no_request"

    def start_requests(self):
        return []


process = CrawlerProcess(settings={})

process.crawl(NoRequestsSpider)
process.start()
