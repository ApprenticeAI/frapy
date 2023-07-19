import warnings
from unittest import TestCase
from urllib.parse import urlparse

from frapy.http import Request, Response
from frapy.spidermiddlewares.offsite import OffsiteMiddleware, PortWarning, URLWarning
from frapy.spiders import Spider
from frapy.utils.test import get_crawler


class TestOffsiteMiddleware(TestCase):
    def setUp(self):
        crawler = get_crawler(Spider)
        self.spider = crawler._create_spider(**self._get_spiderargs())
        self.mw = OffsiteMiddleware.from_crawler(crawler)
        self.mw.spider_opened(self.spider)

    def _get_spiderargs(self):
        return dict(
            name="foo",
            allowed_domains=["frapytest.org", "frapy.org", "frapy.test.org"],
        )

    def test_process_spider_output(self):
        res = Response("http://frapytest.org")

        onsite_reqs = [
            Request("http://frapytest.org/1"),
            Request("http://frapy.org/1"),
            Request("http://sub.frapy.org/1"),
            Request("http://offsite.tld/letmepass", dont_filter=True),
            Request("http://frapy.test.org/"),
            Request("http://frapy.test.org:8000/"),
        ]
        offsite_reqs = [
            Request("http://frapy2.org"),
            Request("http://offsite.tld/"),
            Request("http://offsite.tld/frapytest.org"),
            Request("http://offsite.tld/rogue.frapytest.org"),
            Request("http://rogue.frapytest.org.haha.com"),
            Request("http://roguefrapytest.org"),
            Request("http://test.org/"),
            Request("http://notfrapy.test.org/"),
        ]
        reqs = onsite_reqs + offsite_reqs

        out = list(self.mw.process_spider_output(res, reqs, self.spider))
        self.assertEqual(out, onsite_reqs)


class TestOffsiteMiddleware2(TestOffsiteMiddleware):
    def _get_spiderargs(self):
        return dict(name="foo", allowed_domains=None)

    def test_process_spider_output(self):
        res = Response("http://frapytest.org")
        reqs = [Request("http://a.com/b.html"), Request("http://b.com/1")]
        out = list(self.mw.process_spider_output(res, reqs, self.spider))
        self.assertEqual(out, reqs)


class TestOffsiteMiddleware3(TestOffsiteMiddleware2):
    def _get_spiderargs(self):
        return dict(name="foo")


class TestOffsiteMiddleware4(TestOffsiteMiddleware3):
    def _get_spiderargs(self):
        bad_hostname = urlparse("http:////frapytest.org").hostname
        return dict(name="foo", allowed_domains=["frapytest.org", None, bad_hostname])

    def test_process_spider_output(self):
        res = Response("http://frapytest.org")
        reqs = [Request("http://frapytest.org/1")]
        out = list(self.mw.process_spider_output(res, reqs, self.spider))
        self.assertEqual(out, reqs)


class TestOffsiteMiddleware5(TestOffsiteMiddleware4):
    def test_get_host_regex(self):
        self.spider.allowed_domains = [
            "http://frapytest.org",
            "frapy.org",
            "frapy.test.org",
        ]
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.mw.get_host_regex(self.spider)
            assert issubclass(w[-1].category, URLWarning)


class TestOffsiteMiddleware6(TestOffsiteMiddleware4):
    def test_get_host_regex(self):
        self.spider.allowed_domains = [
            "frapytest.org:8000",
            "frapy.org",
            "frapy.test.org",
        ]
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.mw.get_host_regex(self.spider)
            assert issubclass(w[-1].category, PortWarning)
