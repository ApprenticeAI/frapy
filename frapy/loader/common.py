"""Common functions used in Item Loaders code"""

import warnings

from itemloaders import common

from frapy.utils.deprecate import FrapyDeprecationWarning


def wrap_loader_context(function, context):
    """Wrap functions that receive loader_context to contain the context
    "pre-loaded" and expose a interface that receives only one argument
    """
    warnings.warn(
        "frapy.loader.common.wrap_loader_context has moved to a new library."
        "Please update your reference to itemloaders.common.wrap_loader_context",
        FrapyDeprecationWarning,
        stacklevel=2,
    )

    return common.wrap_loader_context(function, context)
