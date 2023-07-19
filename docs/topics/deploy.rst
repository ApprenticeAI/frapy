.. _topics-deploy:

=================
Deploying Spiders
=================

This section describes the different options you have for deploying your Frapy
spiders to run them on a regular basis. Running Frapy spiders in your local
machine is very convenient for the (early) development stage, but not so much
when you need to execute long-running spiders or move spiders to run in
production continuously. This is where the solutions for deploying Frapy
spiders come in.

Popular choices for deploying Frapy spiders are:

* :ref:`Frapyd <deploy-frapyd>` (open source)
* :ref:`Zyte Frapy Cloud <deploy-frapy-cloud>` (cloud-based)

.. _deploy-frapyd:

Deploying to a Frapyd Server
=============================

`Frapyd`_ is an open source application to run Frapy spiders. It provides
a server with HTTP API, capable of running and monitoring Frapy spiders.

To deploy spiders to Frapyd, you can use the frapyd-deploy tool provided by
the `frapyd-client`_ package. Please refer to the `frapyd-deploy
documentation`_ for more information.

Frapyd is maintained by some of the Frapy developers.

.. _deploy-frapy-cloud:

Deploying to Zyte Frapy Cloud
==============================

`Zyte Frapy Cloud`_ is a hosted, cloud-based service by Zyte_, the company
behind Frapy.

Zyte Frapy Cloud removes the need to setup and monitor servers and provides a
nice UI to manage spiders and review scraped items, logs and stats.

To deploy spiders to Zyte Frapy Cloud you can use the `shub`_ command line
tool.
Please refer to the `Zyte Frapy Cloud documentation`_ for more information.

Zyte Frapy Cloud is compatible with Frapyd and one can switch between
them as needed - the configuration is read from the ``frapy.cfg`` file
just like ``frapyd-deploy``.

.. _Deploying your project: https://frapyd.readthedocs.io/en/latest/deploy.html
.. _Frapyd: https://github.com/frapy/frapyd
.. _frapyd-client: https://github.com/frapy/frapyd-client
.. _frapyd-deploy documentation: https://frapyd.readthedocs.io/en/latest/deploy.html
.. _shub: https://shub.readthedocs.io/en/latest/
.. _Zyte: https://zyte.com/
.. _Zyte Frapy Cloud: https://www.zyte.com/frapy-cloud/
.. _Zyte Frapy Cloud documentation: https://docs.zyte.com/frapy-cloud.html
