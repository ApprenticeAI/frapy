import frapy
from frapy.crawler import CrawlerProcess


class PollReactorSpider(frapy.Spider):
    name = "poll_reactor"


process = CrawlerProcess(
    settings={
        "TWISTED_REACTOR": "twisted.internet.pollreactor.PollReactor",
    }
)
process.crawl(PollReactorSpider)
process.start()
