from unittest import TestCase

import frapy


class ToplevelTestCase(TestCase):
    def test_version(self):
        self.assertIs(type(frapy.__version__), str)

    def test_version_info(self):
        self.assertIs(type(frapy.version_info), tuple)

    def test_request_shortcut(self):
        from frapy.http import FormRequest, Request

        self.assertIs(frapy.Request, Request)
        self.assertIs(frapy.FormRequest, FormRequest)

    def test_spider_shortcut(self):
        from frapy.spiders import Spider

        self.assertIs(frapy.Spider, Spider)

    def test_selector_shortcut(self):
        from frapy.selector import Selector

        self.assertIs(frapy.Selector, Selector)

    def test_item_shortcut(self):
        from frapy.item import Field, Item

        self.assertIs(frapy.Item, Item)
        self.assertIs(frapy.Field, Field)
