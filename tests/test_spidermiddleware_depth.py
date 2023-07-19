from unittest import TestCase

from frapy.http import Request, Response
from frapy.spidermiddlewares.depth import DepthMiddleware
from frapy.spiders import Spider
from frapy.statscollectors import StatsCollector
from frapy.utils.test import get_crawler


class TestDepthMiddleware(TestCase):
    def setUp(self):
        crawler = get_crawler(Spider)
        self.spider = crawler._create_spider("frapytest.org")

        self.stats = StatsCollector(crawler)
        self.stats.open_spider(self.spider)

        self.mw = DepthMiddleware(1, self.stats, True)

    def test_process_spider_output(self):
        req = Request("http://frapytest.org")
        resp = Response("http://frapytest.org")
        resp.request = req
        result = [Request("http://frapytest.org")]

        out = list(self.mw.process_spider_output(resp, result, self.spider))
        self.assertEqual(out, result)

        rdc = self.stats.get_value("request_depth_count/1", spider=self.spider)
        self.assertEqual(rdc, 1)

        req.meta["depth"] = 1

        out2 = list(self.mw.process_spider_output(resp, result, self.spider))
        self.assertEqual(out2, [])

        rdm = self.stats.get_value("request_depth_max", spider=self.spider)
        self.assertEqual(rdm, 1)

    def tearDown(self):
        self.stats.close_spider(self.spider, "")
