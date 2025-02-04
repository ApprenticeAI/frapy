.. _topics-practices:

================
Common Practices
================

This section documents common practices when using Frapy. These are things
that cover many topics and don't often fall into any other specific section.

.. skip: start

.. _run-from-script:

Run Frapy from a script
========================

You can use the :ref:`API <topics-api>` to run Frapy from a script, instead of
the typical way of running Frapy via ``frapy crawl``.

Remember that Frapy is built on top of the Twisted
asynchronous networking library, so you need to run it inside the Twisted reactor.

The first utility you can use to run your spiders is
:class:`frapy.crawler.CrawlerProcess`. This class will start a Twisted reactor
for you, configuring the logging and setting shutdown handlers. This class is
the one used by all Frapy commands.

Here's an example showing how to run a single spider with it.

.. code-block:: python

    import frapy
    from frapy.crawler import CrawlerProcess


    class MySpider(frapy.Spider):
        # Your spider definition
        ...


    process = CrawlerProcess(
        settings={
            "FEEDS": {
                "items.json": {"format": "json"},
            },
        }
    )

    process.crawl(MySpider)
    process.start()  # the script will block here until the crawling is finished

Define settings within dictionary in CrawlerProcess. Make sure to check :class:`~frapy.crawler.CrawlerProcess`
documentation to get acquainted with its usage details.

If you are inside a Frapy project there are some additional helpers you can
use to import those components within the project. You can automatically import
your spiders passing their name to :class:`~frapy.crawler.CrawlerProcess`, and
use ``get_project_settings`` to get a :class:`~frapy.settings.Settings`
instance with your project settings.

What follows is a working example of how to do that, using the `testspiders`_
project as example.

.. code-block:: python

    from frapy.crawler import CrawlerProcess
    from frapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())

    # 'followall' is the name of one of the spiders of the project.
    process.crawl("followall", domain="frapy.org")
    process.start()  # the script will block here until the crawling is finished

There's another Frapy utility that provides more control over the crawling
process: :class:`frapy.crawler.CrawlerRunner`. This class is a thin wrapper
that encapsulates some simple helpers to run multiple crawlers, but it won't
start or interfere with existing reactors in any way.

Using this class the reactor should be explicitly run after scheduling your
spiders. It's recommended you use :class:`~frapy.crawler.CrawlerRunner`
instead of :class:`~frapy.crawler.CrawlerProcess` if your application is
already using Twisted and you want to run Frapy in the same reactor.

Note that you will also have to shutdown the Twisted reactor yourself after the
spider is finished. This can be achieved by adding callbacks to the deferred
returned by the :meth:`CrawlerRunner.crawl
<frapy.crawler.CrawlerRunner.crawl>` method.

Here's an example of its usage, along with a callback to manually stop the
reactor after ``MySpider`` has finished running.

.. code-block:: python

    from twisted.internet import reactor
    import frapy
    from frapy.crawler import CrawlerRunner
    from frapy.utils.log import configure_logging


    class MySpider(frapy.Spider):
        # Your spider definition
        ...


    configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})
    runner = CrawlerRunner()

    d = runner.crawl(MySpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished

.. seealso:: :doc:`twisted:core/howto/reactor-basics`

.. _run-multiple-spiders:

Running multiple spiders in the same process
============================================

By default, Frapy runs a single spider per process when you run ``frapy
crawl``. However, Frapy supports running multiple spiders per process using
the :ref:`internal API <topics-api>`.

Here is an example that runs multiple spiders simultaneously:

.. code-block:: python

    import frapy
    from frapy.crawler import CrawlerProcess
    from frapy.utils.project import get_project_settings


    class MySpider1(frapy.Spider):
        # Your first spider definition
        ...


    class MySpider2(frapy.Spider):
        # Your second spider definition
        ...


    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(MySpider1)
    process.crawl(MySpider2)
    process.start()  # the script will block here until all crawling jobs are finished

Same example using :class:`~frapy.crawler.CrawlerRunner`:

.. code-block:: python

    import frapy
    from twisted.internet import reactor
    from frapy.crawler import CrawlerRunner
    from frapy.utils.log import configure_logging
    from frapy.utils.project import get_project_settings


    class MySpider1(frapy.Spider):
        # Your first spider definition
        ...


    class MySpider2(frapy.Spider):
        # Your second spider definition
        ...


    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(MySpider1)
    runner.crawl(MySpider2)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()  # the script will block here until all crawling jobs are finished

Same example but running the spiders sequentially by chaining the deferreds:

.. code-block:: python

    from twisted.internet import reactor, defer
    from frapy.crawler import CrawlerRunner
    from frapy.utils.log import configure_logging
    from frapy.utils.project import get_project_settings


    class MySpider1(frapy.Spider):
        # Your first spider definition
        ...


    class MySpider2(frapy.Spider):
        # Your second spider definition
        ...


    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)


    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(MySpider1)
        yield runner.crawl(MySpider2)
        reactor.stop()


    crawl()
    reactor.run()  # the script will block here until the last crawl call is finished

Different spiders can set different values for the same setting, but when they
run in the same process it may be impossible, by design or because of some
limitations, to use these different values. What happens in practice is
different for different settings:

* :setting:`SPIDER_LOADER_CLASS` and the ones used by its value
  (:setting:`SPIDER_MODULES`, :setting:`SPIDER_LOADER_WARN_ONLY` for the
  default one) cannot be read from the per-spider settings. These are applied
  when the :class:`~frapy.crawler.CrawlerRunner` or
  :class:`~frapy.crawler.CrawlerProcess` object is created.
* For :setting:`TWISTED_REACTOR` and :setting:`ASYNCIO_EVENT_LOOP` the first
  available value is used, and if a spider requests a different reactor an
  exception will be raised. These are applied when the reactor is installed.
* For :setting:`REACTOR_THREADPOOL_MAXSIZE`, :setting:`DNS_RESOLVER` and the
  ones used by the resolver (:setting:`DNSCACHE_ENABLED`,
  :setting:`DNSCACHE_SIZE`, :setting:`DNS_TIMEOUT` for ones included in Frapy)
  the first available value is used. These are applied when the reactor is
  started.

.. seealso:: :ref:`run-from-script`.

.. skip: end

.. _distributed-crawls:

Distributed crawls
==================

Frapy doesn't provide any built-in facility for running crawls in a distribute
(multi-server) manner. However, there are some ways to distribute crawls, which
vary depending on how you plan to distribute them.

If you have many spiders, the obvious way to distribute the load is to setup
many Frapyd instances and distribute spider runs among those.

If you instead want to run a single (big) spider through many machines, what
you usually do is partition the urls to crawl and send them to each separate
spider. Here is a concrete example:

First, you prepare the list of urls to crawl and put them into separate
files/urls::

    http://somedomain.com/urls-to-crawl/spider1/part1.list
    http://somedomain.com/urls-to-crawl/spider1/part2.list
    http://somedomain.com/urls-to-crawl/spider1/part3.list

Then you fire a spider run on 3 different Frapyd servers. The spider would
receive a (spider) argument ``part`` with the number of the partition to
crawl::

    curl http://frapy1.mycompany.com:6800/schedule.json -d project=myproject -d spider=spider1 -d part=1
    curl http://frapy2.mycompany.com:6800/schedule.json -d project=myproject -d spider=spider1 -d part=2
    curl http://frapy3.mycompany.com:6800/schedule.json -d project=myproject -d spider=spider1 -d part=3

.. _bans:

Avoiding getting banned
=======================

Some websites implement certain measures to prevent bots from crawling them,
with varying degrees of sophistication. Getting around those measures can be
difficult and tricky, and may sometimes require special infrastructure. Please
consider contacting `commercial support`_ if in doubt.

Here are some tips to keep in mind when dealing with these kinds of sites:

* rotate your user agent from a pool of well-known ones from browsers (google
  around to get a list of them)
* disable cookies (see :setting:`COOKIES_ENABLED`) as some sites may use
  cookies to spot bot behaviour
* use download delays (2 or higher). See :setting:`DOWNLOAD_DELAY` setting.
* if possible, use `Common Crawl`_ to fetch pages, instead of hitting the sites
  directly
* use a pool of rotating IPs. For example, the free `Tor project`_ or paid
  services like `ProxyMesh`_. An open source alternative is `scrapoxy`_, a
  super proxy that you can attach your own proxies to.
* use a highly distributed downloader that circumvents bans internally, so you
  can just focus on parsing clean pages. One example of such downloaders is
  `Zyte Smart Proxy Manager`_

If you are still unable to prevent your bot getting banned, consider contacting
`commercial support`_.

.. _Tor project: https://www.torproject.org/
.. _commercial support: https://frapy.org/support/
.. _ProxyMesh: https://proxymesh.com/
.. _Common Crawl: https://commoncrawl.org/
.. _testspiders: https://github.com/scrapinghub/testspiders
.. _scrapoxy: https://scrapoxy.io/
.. _Zyte Smart Proxy Manager: https://www.zyte.com/smart-proxy-manager/
