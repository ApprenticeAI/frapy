import frapy
from frapy.crawler import CrawlerProcess


class AsyncioReactorSpider(frapy.Spider):
    name = "asyncio_reactor"


process = CrawlerProcess(
    settings={
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }
)
process.crawl(AsyncioReactorSpider)
process.start()
