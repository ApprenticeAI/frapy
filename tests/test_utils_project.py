import contextlib
import os
import shutil
import tempfile
import unittest
import warnings
from pathlib import Path

from frapy.utils.project import data_path, get_project_settings


@contextlib.contextmanager
def inside_a_project():
    prev_dir = os.getcwd()
    project_dir = tempfile.mkdtemp()

    try:
        os.chdir(project_dir)
        Path("frapy.cfg").touch()

        yield project_dir
    finally:
        os.chdir(prev_dir)
        shutil.rmtree(project_dir)


class ProjectUtilsTest(unittest.TestCase):
    def test_data_path_outside_project(self):
        self.assertEqual(str(Path(".frapy", "somepath")), data_path("somepath"))
        abspath = str(Path(os.path.sep, "absolute", "path"))
        self.assertEqual(abspath, data_path(abspath))

    def test_data_path_inside_project(self):
        with inside_a_project() as proj_path:
            expected = Path(proj_path, ".frapy", "somepath")
            self.assertEqual(expected.resolve(), Path(data_path("somepath")).resolve())
            abspath = str(Path(os.path.sep, "absolute", "path").resolve())
            self.assertEqual(abspath, data_path(abspath))


@contextlib.contextmanager
def set_env(**update):
    modified = set(update.keys()) & set(os.environ.keys())
    update_after = {k: os.environ[k] for k in modified}
    remove_after = frozenset(k for k in update if k not in os.environ)
    try:
        os.environ.update(update)
        yield
    finally:
        os.environ.update(update_after)
        for k in remove_after:
            os.environ.pop(k)


class GetProjectSettingsTestCase(unittest.TestCase):
    def test_valid_envvar(self):
        value = "tests.test_cmdline.settings"
        envvars = {
            "FRAPY_SETTINGS_MODULE": value,
        }
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            with set_env(**envvars):
                settings = get_project_settings()

        assert settings.get("SETTINGS_MODULE") == value

    def test_invalid_envvar(self):
        envvars = {
            "FRAPY_FOO": "bar",
        }
        with set_env(**envvars):
            settings = get_project_settings()

        assert settings.get("FRAPY_FOO") is None

    def test_valid_and_invalid_envvars(self):
        value = "tests.test_cmdline.settings"
        envvars = {
            "FRAPY_FOO": "bar",
            "FRAPY_SETTINGS_MODULE": value,
        }
        with set_env(**envvars):
            settings = get_project_settings()
        assert settings.get("SETTINGS_MODULE") == value
        assert settings.get("FRAPY_FOO") is None
