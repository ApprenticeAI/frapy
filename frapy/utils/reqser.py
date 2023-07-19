import warnings
from typing import Optional

import frapy
from frapy.exceptions import FrapyDeprecationWarning
from frapy.utils.request import request_from_dict as _from_dict

warnings.warn(
    (
        "Module frapy.utils.reqser is deprecated, please use request.to_dict method"
        " and/or frapy.utils.request.request_from_dict instead"
    ),
    category=FrapyDeprecationWarning,
    stacklevel=2,
)


def request_to_dict(
    request: "frapy.Request", spider: Optional["frapy.Spider"] = None
) -> dict:
    return request.to_dict(spider=spider)


def request_from_dict(
    d: dict, spider: Optional["frapy.Spider"] = None
) -> "frapy.Request":
    return _from_dict(d, spider=spider)
