import asyncio
import sys

from twisted.internet import asyncioreactor
from uvloop import Loop

if sys.version_info >= (3, 8) and sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.set_event_loop(Loop())
asyncioreactor.install(asyncio.get_event_loop())

import frapy  # noqa: E402
from frapy.crawler import CrawlerProcess  # noqa: E402


class NoRequestsSpider(frapy.Spider):
    name = "no_request"

    def start_requests(self):
        return []


process = CrawlerProcess(
    settings={
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "ASYNCIO_EVENT_LOOP": "uvloop.Loop",
    }
)
process.crawl(NoRequestsSpider)
process.start()
