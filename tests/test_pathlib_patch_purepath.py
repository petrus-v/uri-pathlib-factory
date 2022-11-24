import os

if os.name == "nt":
    from pathlib import PureWindowsPath as PureOsPath
else:
    from pathlib import PurePosixPath as PureOsPath

from pathlib import PurePath

from uri_pathlib_factory.main import original_purepath_new, unload_pathlib_monkey_patch

from .pathlib_test_uri_backend import PureTestPath


def test_load_unload_pure_path_patch(pathlib_monkey_patch):
    assert PurePath.__new__ is not original_purepath_new
    unload_pathlib_monkey_patch()
    assert PurePath.__new__ is original_purepath_new


def test_pure_test_path(pathlib_monkey_patch, mock_entry_points_path):
    assert PurePath("test://something").__class__ is PureTestPath


def test_empty_purepath(pathlib_monkey_patch):
    assert PurePath().__class__ is PureOsPath


def test_relative_purepath(pathlib_monkey_patch):
    assert PurePath("./test").__class__ is PureOsPath


def test_concatenate_purepath(pathlib_monkey_patch, mock_entry_points_path):
    assert (PurePath("test:///test") / "other").__class__ is PureTestPath
    assert (PurePath("test:///test") / PurePath("other")).__class__ is PureTestPath
    assert PurePath(PurePath("test:///main")).__class__ is PureTestPath

    assert (PurePath("/test") / "other").__class__ is PureOsPath
    assert (PurePath("/test") / PurePath("other")).__class__ is PureOsPath
    assert ("other" / PurePath("/test")).__class__ is PureOsPath
    assert ("test://" / PurePath("/test")).__class__ is PureOsPath


def test_instantiate_test_pure_path_with_patch(
    pathlib_monkey_patch, mock_entry_points_path
):
    assert PureTestPath("/main").__class__ is PureTestPath
    assert PureTestPath("/main").as_uri() == "test:///main"
