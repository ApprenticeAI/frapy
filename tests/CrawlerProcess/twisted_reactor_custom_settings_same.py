import frapy
from frapy.crawler import CrawlerProcess


class AsyncioReactorSpider1(frapy.Spider):
    name = "asyncio_reactor1"
    custom_settings = {
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }


class AsyncioReactorSpider2(frapy.Spider):
    name = "asyncio_reactor2"
    custom_settings = {
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }


process = CrawlerProcess()
process.crawl(AsyncioReactorSpider1)
process.crawl(AsyncioReactorSpider2)
process.start()
