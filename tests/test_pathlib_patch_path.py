import os

if os.name == "nt":
    from pathlib import WindowsPath as OsPath
else:
    from pathlib import PosixPath as OsPath

from pathlib import Path

from uri_pathlib_factory.main import original_path_new, unload_pathlib_monkey_patch

from .pathlib_test_uri_backend import TestPath


def test_load_unload_path_patch(pathlib_monkey_patch):
    assert Path.__new__ is not original_path_new
    unload_pathlib_monkey_patch()
    assert Path.__new__ is original_path_new


def test_test_path(pathlib_monkey_patch, mock_entry_points_path):
    assert Path("test://something").__class__ is TestPath


def test_empty_path(pathlib_monkey_patch):
    assert Path().__class__ is OsPath


def test_relative_path(pathlib_monkey_patch):
    assert Path("./test").__class__ is OsPath


def test_concatenate_posix(pathlib_monkey_patch, mock_entry_points_path):
    assert (Path("test:///test") / "other").__class__ is TestPath
    assert (Path("test:///test") / Path("other")).__class__ is TestPath
    assert Path(Path("test:///test")).__class__ is TestPath

    assert (Path("/test") / "other").__class__ is OsPath
    assert (Path("/test") / Path("other")).__class__ is OsPath
    assert ("other" / Path("/test")).__class__ is OsPath
    assert ("test://" / Path("/test")).__class__ is OsPath


def test_instantiate_test_path_with_patch(pathlib_monkey_patch, mock_entry_points_path):
    assert TestPath("/main").__class__ is TestPath
    assert TestPath("/main").as_uri() == "test:///main"
