import frapy
from frapy.crawler import CrawlerProcess


class CachingHostnameResolverSpider(frapy.Spider):
    """
    Finishes without a twisted.internet.error.DNSLookupError exception
    """

    name = "caching_hostname_resolver_spider"
    start_urls = ["http://[::1]"]


if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "RETRY_ENABLED": False,
            "DNS_RESOLVER": "frapy.resolver.CachingHostnameResolver",
        }
    )
    process.crawl(CachingHostnameResolverSpider)
    process.start()
