"""
MemoryDebugger extension

See documentation in docs/topics/extensions.rst
"""

import gc

from frapy import signals
from frapy.exceptions import NotConfigured
from frapy.utils.trackref import live_refs


class MemoryDebugger:
    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool("MEMDEBUG_ENABLED"):
            raise NotConfigured
        o = cls(crawler.stats)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_closed(self, spider, reason):
        gc.collect()
        self.stats.set_value(
            "memdebug/gc_garbage_count", len(gc.garbage), spider=spider
        )
        for cls, wdict in live_refs.items():
            if not wdict:
                continue
            self.stats.set_value(
                f"memdebug/live_refs/{cls.__name__}", len(wdict), spider=spider
            )
