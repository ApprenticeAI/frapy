from tests.test_commands import CommandTest


class CheckCommandTest(CommandTest):
    command = "check"

    def setUp(self):
        super().setUp()
        self.spider_name = "check_spider"
        self.spider = (self.proj_mod_path / "spiders" / "checkspider.py").resolve()

    def _write_contract(self, contracts, parse_def):
        self.spider.write_text(
            f"""
import frapy

class CheckSpider(frapy.Spider):
    name = '{self.spider_name}'
    start_urls = ['http://toscrape.com']

    def parse(self, response, **cb_kwargs):
        \"\"\"
        @url http://toscrape.com
        {contracts}
        \"\"\"
        {parse_def}
        """,
            encoding="utf-8",
        )

    def _test_contract(self, contracts="", parse_def="pass"):
        self._write_contract(contracts, parse_def)
        p, out, err = self.proc("check")
        self.assertNotIn("F", out)
        self.assertIn("OK", err)
        self.assertEqual(p.returncode, 0)

    def test_check_returns_requests_contract(self):
        contracts = """
        @returns requests 1
        """
        parse_def = """
        yield frapy.Request(url='http://next-url.com')
        """
        self._test_contract(contracts, parse_def)

    def test_check_returns_items_contract(self):
        contracts = """
        @returns items 1
        """
        parse_def = """
        yield {'key1': 'val1', 'key2': 'val2'}
        """
        self._test_contract(contracts, parse_def)

    def test_check_cb_kwargs_contract(self):
        contracts = """
        @cb_kwargs {"arg1": "val1", "arg2": "val2"}
        """
        parse_def = """
        if len(cb_kwargs.items()) == 0:
            raise Exception("Callback args not set")
        """
        self._test_contract(contracts, parse_def)

    def test_check_scrapes_contract(self):
        contracts = """
        @scrapes key1 key2
        """
        parse_def = """
        yield {'key1': 'val1', 'key2': 'val2'}
        """
        self._test_contract(contracts, parse_def)

    def test_check_all_default_contracts(self):
        contracts = """
        @returns items 1
        @returns requests 1
        @scrapes key1 key2
        @cb_kwargs {"arg1": "val1", "arg2": "val2"}
        """
        parse_def = """
        yield {'key1': 'val1', 'key2': 'val2'}
        yield frapy.Request(url='http://next-url.com')
        if len(cb_kwargs.items()) == 0:
            raise Exception("Callback args not set")
        """
        self._test_contract(contracts, parse_def)

    def test_FRAPY_CHECK_set(self):
        parse_def = """
        import os
        if not os.environ.get('FRAPY_CHECK'):
            raise Exception('FRAPY_CHECK not set')
        """
        self._test_contract(parse_def=parse_def)
