import os

if os.name == "nt":
    from pathlib import WindowsPath as OsPath
else:
    from pathlib import PosixPath as OsPath

import pytest

from uri_pathlib_factory import PathFactory

from .pathlib_test_uri_backend import TestPath


@pytest.mark.parametrize(
    "path,expected_class,expected_str_value,expected_uri_value",
    [
        pytest.param(
            "/",
            OsPath,
            "/",
            "file:///",
            marks=pytest.mark.skipif(
                os.name == "nt", reason="NT os raise value error on relative path"
            ),
        ),
        pytest.param(
            "/home/pverkest",
            OsPath,
            "/home/pverkest",
            "file:///home/pverkest",
            marks=pytest.mark.skipif(
                os.name == "nt", reason="NT os raise value error on relative path"
            ),
        ),
        (
            "test:///path/test/backend",
            TestPath,
            "/extra/path/test/backend",
            "test:///extra/path/test/backend",
        ),
        (
            "test2:///path/test/backend",
            TestPath,
            "/path/test/backend",
            "test:///path/test/backend",
        ),
        (
            "test2://path/test/backend",
            TestPath,
            "/path/test/backend",
            "test:///path/test/backend",
        ),
        (
            "test2:/path/test/backend",
            TestPath,
            "/path/test/backend",
            "test:///path/test/backend",
        ),
    ],
)
def test_pure_path_factory(
    reloaded_plugin_registry_with_test_plugin,
    path,
    expected_class,
    expected_str_value,
    expected_uri_value,
):
    pure_path = PathFactory(path)

    assert pure_path.__class__ is expected_class
    assert str(pure_path) == expected_str_value
    assert pure_path.as_uri() == expected_uri_value


def test_path_factory_concatenate(reloaded_plugin_registry_with_test_plugin):
    assert (PathFactory("test:///test") / "other").__class__ is TestPath
    assert (PathFactory("test:///test") / PathFactory("other")).__class__ is TestPath
    assert PathFactory(PathFactory("test:///test")).__class__ is TestPath

    assert (PathFactory("/test") / "other").__class__ is OsPath
    assert (PathFactory("/test") / PathFactory("other")).__class__ is OsPath
    assert ("other" / PathFactory("/test")).__class__ is OsPath
    assert ("test://" / PathFactory("/test")).__class__ is OsPath
