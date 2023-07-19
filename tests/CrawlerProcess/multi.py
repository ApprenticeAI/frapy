import frapy
from frapy.crawler import CrawlerProcess


class NoRequestsSpider(frapy.Spider):
    name = "no_request"

    def start_requests(self):
        return []


process = CrawlerProcess(settings={})

process.crawl(NoRequestsSpider)
process.crawl(NoRequestsSpider)
process.start()
