import sys

from twisted.internet import defer
from twisted.trial import unittest

import frapy
from frapy.utils.testproc import ProcessTest


class VersionTest(ProcessTest, unittest.TestCase):
    command = "version"

    @defer.inlineCallbacks
    def test_output(self):
        encoding = getattr(sys.stdout, "encoding") or "utf-8"
        _, out, _ = yield self.execute([])
        self.assertEqual(
            out.strip().decode(encoding),
            f"Frapy {frapy.__version__}",
        )

    @defer.inlineCallbacks
    def test_verbose_output(self):
        encoding = getattr(sys.stdout, "encoding") or "utf-8"
        _, out, _ = yield self.execute(["-v"])
        headers = [
            line.partition(":")[0].strip()
            for line in out.strip().decode(encoding).splitlines()
        ]
        self.assertEqual(
            headers,
            [
                "Frapy",
                "lxml",
                "libxml2",
                "cssselect",
                "parsel",
                "w3lib",
                "Twisted",
                "Python",
                "pyOpenSSL",
                "cryptography",
                "Platform",
            ],
        )
