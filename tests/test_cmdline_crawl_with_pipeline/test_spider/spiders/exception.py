import frapy


class ExceptionSpider(frapy.Spider):
    name = "exception"

    custom_settings = {
        "ITEM_PIPELINES": {"test_spider.pipelines.TestSpiderExceptionPipeline": 300}
    }

    def parse(self, response):
        pass
