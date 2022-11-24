import os

import pytest

if os.name == "nt":
    from pathlib import PureWindowsPath as PureOsPath
else:
    from pathlib import PurePosixPath as PureOsPath

from uri_pathlib_factory import PurePathFactory

from .pathlib_test_uri_backend import PureTestPath


@pytest.mark.parametrize(
    "path,expected_class,expected_str_value,expected_uri_value",
    [
        pytest.param(
            "/",
            PureOsPath,
            "/",
            "file:///",
            marks=pytest.mark.skipif(
                os.name == "nt", reason="NT os raise value error on relative path"
            ),
        ),
        pytest.param(
            "/home/pverkest",
            PureOsPath,
            "/home/pverkest",
            "file:///home/pverkest",
            marks=pytest.mark.skipif(
                os.name == "nt", reason="NT os raise value error on relative path"
            ),
        ),
        (
            "test:///path/test/backend",
            PureTestPath,
            "/extra/path/test/backend",
            "test:///extra/path/test/backend",
        ),
        (
            "test2:///path/test/backend",
            PureTestPath,
            "/path/test/backend",
            "test:///path/test/backend",
        ),
        (
            "test2://path/test/backend",
            PureTestPath,
            "/path/test/backend",
            "test:///path/test/backend",
        ),
        (
            "test2:/path/test/backend",
            PureTestPath,
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
    pure_path = PurePathFactory(path)

    assert pure_path.__class__ is expected_class
    assert str(pure_path) == expected_str_value
    assert pure_path.as_uri() == expected_uri_value


def test_pure_path_factory_concatenate(reloaded_plugin_registry_with_test_plugin):
    assert (PurePathFactory("test:///test") / "other").__class__ is PureTestPath
    assert (
        PurePathFactory("test:///test") / PurePathFactory("other")
    ).__class__ is PureTestPath
    assert PurePathFactory(PurePathFactory("test:///test")).__class__ is PureTestPath

    assert (PurePathFactory("/test") / "other").__class__ is PureOsPath
    assert (PurePathFactory("/test") / PurePathFactory("other")).__class__ is PureOsPath
    assert ("other" / PurePathFactory("/test")).__class__ is PureOsPath
    assert ("test://" / PurePathFactory("/test")).__class__ is PureOsPath
