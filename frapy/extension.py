"""
The Extension Manager

See documentation in docs/topics/extensions.rst
"""
from frapy.middleware import MiddlewareManager
from frapy.utils.conf import build_component_list


class ExtensionManager(MiddlewareManager):
    component_name = "extension"

    @classmethod
    def _get_mwlist_from_settings(cls, settings):
        return build_component_list(settings.getwithbase("EXTENSIONS"))
