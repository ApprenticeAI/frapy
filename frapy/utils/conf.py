import numbers
import os
import sys
import warnings
from configparser import ConfigParser
from operator import itemgetter
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from frapy.exceptions import FrapyDeprecationWarning, UsageError
from frapy.settings import BaseSettings
from frapy.utils.deprecate import update_classpath
from frapy.utils.python import without_none_values


def build_component_list(compdict, custom=None, convert=update_classpath):
    """Compose a component list from a { class: order } dictionary."""

    def _check_components(complist):
        if len({convert(c) for c in complist}) != len(complist):
            raise ValueError(
                f"Some paths in {complist!r} convert to the same object, "
                "please update your settings"
            )

    def _map_keys(compdict):
        if isinstance(compdict, BaseSettings):
            compbs = BaseSettings()
            for k, v in compdict.items():
                prio = compdict.getpriority(k)
                if compbs.getpriority(convert(k)) == prio:
                    raise ValueError(
                        f"Some paths in {list(compdict.keys())!r} "
                        "convert to the same "
                        "object, please update your settings"
                    )
                else:
                    compbs.set(convert(k), v, priority=prio)
            return compbs
        _check_components(compdict)
        return {convert(k): v for k, v in compdict.items()}

    def _validate_values(compdict):
        """Fail if a value in the components dict is not a real number or None."""
        for name, value in compdict.items():
            if value is not None and not isinstance(value, numbers.Real):
                raise ValueError(
                    f"Invalid value {value} for component {name}, "
                    "please provide a real number or None instead"
                )

    if isinstance(custom, (list, tuple)):
        _check_components(custom)
        return type(custom)(convert(c) for c in custom)

    if custom is not None:
        compdict.update(custom)

    _validate_values(compdict)
    compdict = without_none_values(_map_keys(compdict))
    return [k for k, v in sorted(compdict.items(), key=itemgetter(1))]


def arglist_to_dict(arglist):
    """Convert a list of arguments like ['arg1=val1', 'arg2=val2', ...] to a
    dict
    """
    return dict(x.split("=", 1) for x in arglist)


def closest_frapy_cfg(
    path: Union[str, os.PathLike] = ".",
    prevpath: Optional[Union[str, os.PathLike]] = None,
) -> str:
    """Return the path to the closest frapy.cfg file by traversing the current
    directory and its parents
    """
    if prevpath is not None and str(path) == str(prevpath):
        return ""
    path = Path(path).resolve()
    cfgfile = path / "frapy.cfg"
    if cfgfile.exists():
        return str(cfgfile)
    return closest_frapy_cfg(path.parent, path)


def init_env(project="default", set_syspath=True):
    """Initialize environment to use command-line tool from inside a project
    dir. This sets the Frapy settings module and modifies the Python path to
    be able to locate the project module.
    """
    cfg = get_config()
    if cfg.has_option("settings", project):
        os.environ["FRAPY_SETTINGS_MODULE"] = cfg.get("settings", project)
    closest = closest_frapy_cfg()
    if closest:
        projdir = str(Path(closest).parent)
        if set_syspath and projdir not in sys.path:
            sys.path.append(projdir)


def get_config(use_closest=True):
    """Get Frapy config file as a ConfigParser"""
    sources = get_sources(use_closest)
    cfg = ConfigParser()
    cfg.read(sources)
    return cfg


def get_sources(use_closest=True) -> List[str]:
    xdg_config_home = (
        os.environ.get("XDG_CONFIG_HOME") or Path("~/.config").expanduser()
    )
    sources = [
        "/etc/frapy.cfg",
        r"c:\frapy\frapy.cfg",
        str(Path(xdg_config_home) / "frapy.cfg"),
        str(Path("~/.frapy.cfg").expanduser()),
    ]
    if use_closest:
        sources.append(closest_frapy_cfg())
    return sources


def feed_complete_default_values_from_settings(feed, settings):
    out = feed.copy()
    out.setdefault("batch_item_count", settings.getint("FEED_EXPORT_BATCH_ITEM_COUNT"))
    out.setdefault("encoding", settings["FEED_EXPORT_ENCODING"])
    out.setdefault("fields", settings.getdictorlist("FEED_EXPORT_FIELDS") or None)
    out.setdefault("store_empty", settings.getbool("FEED_STORE_EMPTY"))
    out.setdefault("uri_params", settings["FEED_URI_PARAMS"])
    out.setdefault("item_export_kwargs", {})
    if settings["FEED_EXPORT_INDENT"] is None:
        out.setdefault("indent", None)
    else:
        out.setdefault("indent", settings.getint("FEED_EXPORT_INDENT"))
    return out


def feed_process_params_from_cli(
    settings,
    output: List[str],
    output_format=None,
    overwrite_output: Optional[List[str]] = None,
):
    """
    Receives feed export params (from the 'crawl' or 'runspider' commands),
    checks for inconsistencies in their quantities and returns a dictionary
    suitable to be used as the FEEDS setting.
    """
    valid_output_formats = without_none_values(
        settings.getwithbase("FEED_EXPORTERS")
    ).keys()

    def check_valid_format(output_format):
        if output_format not in valid_output_formats:
            raise UsageError(
                f"Unrecognized output format '{output_format}'. "
                f"Set a supported one ({tuple(valid_output_formats)}) "
                "after a colon at the end of the output URI (i.e. -o/-O "
                "<URI>:<FORMAT>) or as a file extension."
            )

    overwrite = False
    if overwrite_output:
        if output:
            raise UsageError(
                "Please use only one of -o/--output and -O/--overwrite-output"
            )
        if output_format:
            raise UsageError(
                "-t/--output-format is a deprecated command line option"
                " and does not work in combination with -O/--overwrite-output."
                " To specify a format please specify it after a colon at the end of the"
                " output URI (i.e. -O <URI>:<FORMAT>)."
                " Example working in the tutorial: "
                "frapy crawl quotes -O quotes.json:json"
            )
        output = overwrite_output
        overwrite = True

    if output_format:
        if len(output) == 1:
            check_valid_format(output_format)
            message = (
                "The -t/--output-format command line option is deprecated in favor of "
                "specifying the output format within the output URI using the -o/--output or the"
                " -O/--overwrite-output option (i.e. -o/-O <URI>:<FORMAT>). See the documentation"
                " of the -o or -O option or the following examples for more information. "
                "Examples working in the tutorial: "
                "frapy crawl quotes -o quotes.csv:csv   or   "
                "frapy crawl quotes -O quotes.json:json"
            )
            warnings.warn(message, FrapyDeprecationWarning, stacklevel=2)
            return {output[0]: {"format": output_format}}
        raise UsageError(
            "The -t command-line option cannot be used if multiple output "
            "URIs are specified"
        )

    result: Dict[str, Dict[str, Any]] = {}
    for element in output:
        try:
            feed_uri, feed_format = element.rsplit(":", 1)
        except ValueError:
            feed_uri = element
            feed_format = Path(element).suffix.replace(".", "")
        else:
            if feed_uri == "-":
                feed_uri = "stdout:"
        check_valid_format(feed_format)
        result[feed_uri] = {"format": feed_format}
        if overwrite:
            result[feed_uri]["overwrite"] = True

    # FEEDS setting should take precedence over the matching CLI options
    result.update(settings.getdict("FEEDS"))

    return result
