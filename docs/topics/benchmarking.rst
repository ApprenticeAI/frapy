.. _benchmarking:

============
Benchmarking
============

Frapy comes with a simple benchmarking suite that spawns a local HTTP server
and crawls it at the maximum possible speed. The goal of this benchmarking is
to get an idea of how Frapy performs in your hardware, in order to have a
common baseline for comparisons. It uses a simple spider that does nothing and
just follows links.

To run it use::

    frapy bench

You should see an output like this::

    2016-12-16 21:18:48 [frapy.utils.log] INFO: Frapy 1.2.2 started (bot: quotesbot)
    2016-12-16 21:18:48 [frapy.utils.log] INFO: Overridden settings: {'CLOSESPIDER_TIMEOUT': 10, 'ROBOTSTXT_OBEY': True, 'SPIDER_MODULES': ['quotesbot.spiders'], 'LOGSTATS_INTERVAL': 1, 'BOT_NAME': 'quotesbot', 'LOG_LEVEL': 'INFO', 'NEWSPIDER_MODULE': 'quotesbot.spiders'}
    2016-12-16 21:18:49 [frapy.middleware] INFO: Enabled extensions:
    ['frapy.extensions.closespider.CloseSpider',
     'frapy.extensions.logstats.LogStats',
     'frapy.extensions.telnet.TelnetConsole',
     'frapy.extensions.corestats.CoreStats']
    2016-12-16 21:18:49 [frapy.middleware] INFO: Enabled downloader middlewares:
    ['frapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware',
     'frapy.downloadermiddlewares.httpauth.HttpAuthMiddleware',
     'frapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware',
     'frapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware',
     'frapy.downloadermiddlewares.useragent.UserAgentMiddleware',
     'frapy.downloadermiddlewares.retry.RetryMiddleware',
     'frapy.downloadermiddlewares.redirect.MetaRefreshMiddleware',
     'frapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware',
     'frapy.downloadermiddlewares.redirect.RedirectMiddleware',
     'frapy.downloadermiddlewares.cookies.CookiesMiddleware',
     'frapy.downloadermiddlewares.stats.DownloaderStats']
    2016-12-16 21:18:49 [frapy.middleware] INFO: Enabled spider middlewares:
    ['frapy.spidermiddlewares.httperror.HttpErrorMiddleware',
     'frapy.spidermiddlewares.offsite.OffsiteMiddleware',
     'frapy.spidermiddlewares.referer.RefererMiddleware',
     'frapy.spidermiddlewares.urllength.UrlLengthMiddleware',
     'frapy.spidermiddlewares.depth.DepthMiddleware']
    2016-12-16 21:18:49 [frapy.middleware] INFO: Enabled item pipelines:
    []
    2016-12-16 21:18:49 [frapy.core.engine] INFO: Spider opened
    2016-12-16 21:18:49 [frapy.extensions.logstats] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
    2016-12-16 21:18:50 [frapy.extensions.logstats] INFO: Crawled 70 pages (at 4200 pages/min), scraped 0 items (at 0 items/min)
    2016-12-16 21:18:51 [frapy.extensions.logstats] INFO: Crawled 134 pages (at 3840 pages/min), scraped 0 items (at 0 items/min)
    2016-12-16 21:18:52 [frapy.extensions.logstats] INFO: Crawled 198 pages (at 3840 pages/min), scraped 0 items (at 0 items/min)
    2016-12-16 21:18:53 [frapy.extensions.logstats] INFO: Crawled 254 pages (at 3360 pages/min), scraped 0 items (at 0 items/min)
    2016-12-16 21:18:54 [frapy.extensions.logstats] INFO: Crawled 302 pages (at 2880 pages/min), scraped 0 items (at 0 items/min)
    2016-12-16 21:18:55 [frapy.extensions.logstats] INFO: Crawled 358 pages (at 3360 pages/min), scraped 0 items (at 0 items/min)
    2016-12-16 21:18:56 [frapy.extensions.logstats] INFO: Crawled 406 pages (at 2880 pages/min), scraped 0 items (at 0 items/min)
    2016-12-16 21:18:57 [frapy.extensions.logstats] INFO: Crawled 438 pages (at 1920 pages/min), scraped 0 items (at 0 items/min)
    2016-12-16 21:18:58 [frapy.extensions.logstats] INFO: Crawled 470 pages (at 1920 pages/min), scraped 0 items (at 0 items/min)
    2016-12-16 21:18:59 [frapy.core.engine] INFO: Closing spider (closespider_timeout)
    2016-12-16 21:18:59 [frapy.extensions.logstats] INFO: Crawled 518 pages (at 2880 pages/min), scraped 0 items (at 0 items/min)
    2016-12-16 21:19:00 [frapy.statscollectors] INFO: Dumping Frapy stats:
    {'downloader/request_bytes': 229995,
     'downloader/request_count': 534,
     'downloader/request_method_count/GET': 534,
     'downloader/response_bytes': 1565504,
     'downloader/response_count': 534,
     'downloader/response_status_count/200': 534,
     'finish_reason': 'closespider_timeout',
     'finish_time': datetime.datetime(2016, 12, 16, 16, 19, 0, 647725),
     'log_count/INFO': 17,
     'request_depth_max': 19,
     'response_received_count': 534,
     'scheduler/dequeued': 533,
     'scheduler/dequeued/memory': 533,
     'scheduler/enqueued': 10661,
     'scheduler/enqueued/memory': 10661,
     'start_time': datetime.datetime(2016, 12, 16, 16, 18, 49, 799869)}
    2016-12-16 21:19:00 [frapy.core.engine] INFO: Spider closed (closespider_timeout)

That tells you that Frapy is able to crawl about 3000 pages per minute in the
hardware where you run it. Note that this is a very simple spider intended to
follow links, any custom spider you write will probably do more stuff which
results in slower crawl rates. How slower depends on how much your spider does
and how well it's written.

Use frapy-bench_ for more complex benchmarking.

.. _frapy-bench: https://github.com/frapy/frapy-bench