import os
import warnings
from importlib import import_module
from pathlib import Path

from frapy.exceptions import NotConfigured
from frapy.settings import Settings
from frapy.utils.conf import closest_frapy_cfg, get_config, init_env

ENVVAR = "SCRAPY_SETTINGS_MODULE"
DATADIR_CFG_SECTION = "datadir"


def inside_project():
    frapy_module = os.environ.get("SCRAPY_SETTINGS_MODULE")
    if frapy_module is not None:
        try:
            import_module(frapy_module)
        except ImportError as exc:
            warnings.warn(
                f"Cannot import frapy settings module {frapy_module}: {exc}"
            )
        else:
            return True
    return bool(closest_frapy_cfg())


def project_data_dir(project="default") -> str:
    """Return the current project data dir, creating it if it doesn't exist"""
    if not inside_project():
        raise NotConfigured("Not inside a project")
    cfg = get_config()
    if cfg.has_option(DATADIR_CFG_SECTION, project):
        d = Path(cfg.get(DATADIR_CFG_SECTION, project))
    else:
        frapy_cfg = closest_frapy_cfg()
        if not frapy_cfg:
            raise NotConfigured(
                "Unable to find frapy.cfg file to infer project data dir"
            )
        d = (Path(frapy_cfg).parent / ".frapy").resolve()
    if not d.exists():
        d.mkdir(parents=True)
    return str(d)


def data_path(path: str, createdir=False) -> str:
    """
    Return the given path joined with the .frapy data directory.
    If given an absolute path, return it unmodified.
    """
    path_obj = Path(path)
    if not path_obj.is_absolute():
        if inside_project():
            path_obj = Path(project_data_dir(), path)
        else:
            path_obj = Path(".frapy", path)
    if createdir and not path_obj.exists():
        path_obj.mkdir(parents=True)
    return str(path_obj)


def get_project_settings():
    if ENVVAR not in os.environ:
        project = os.environ.get("SCRAPY_PROJECT", "default")
        init_env(project)

    settings = Settings()
    settings_module_path = os.environ.get(ENVVAR)
    if settings_module_path:
        settings.setmodule(settings_module_path, priority="project")

    valid_envvars = {
        "CHECK",
        "PROJECT",
        "PYTHON_SHELL",
        "SETTINGS_MODULE",
    }

    frapy_envvars = {
        k[7:]: v
        for k, v in os.environ.items()
        if k.startswith("SCRAPY_") and k.replace("SCRAPY_", "") in valid_envvars
    }

    settings.setdict(frapy_envvars, priority="project")

    return settings
