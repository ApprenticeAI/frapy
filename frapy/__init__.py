"""
Frapy - a web crawling and web scraping framework written for Python
"""

import pkgutil
import sys
import warnings

from twisted import version as _txv

# Declare top-level shortcuts
from frapy.http import FormRequest, Request
from frapy.item import Field, Item
from frapy.selector import Selector
from frapy.spiders import Spider

__all__ = [
    "__version__",
    "version_info",
    "twisted_version",
    "Spider",
    "Request",
    "FormRequest",
    "Selector",
    "Item",
    "Field",
]


# Frapy and Twisted versions
__version__ = (pkgutil.get_data(__package__, "VERSION") or b"").decode("ascii").strip()
version_info = tuple(int(v) if v.isdigit() else v for v in __version__.split("."))
twisted_version = (_txv.major, _txv.minor, _txv.micro)


# Check minimum required Python version
if sys.version_info < (3, 7):
    print(f"Frapy {__version__} requires Python 3.7+")
    sys.exit(1)


# Ignore noisy twisted deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="twisted")


del pkgutil
del sys
del warnings