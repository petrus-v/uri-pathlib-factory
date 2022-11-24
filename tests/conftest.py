import sys

import pytest

from uri_pathlib_factory.main import (
    load_pathlib_monkey_patch,
    load_uri_backends_from_plugins,
    unload_pathlib_monkey_patch,
)

if sys.version_info < (3, 10):
    from importlib_metadata import EntryPoint
else:
    from importlib.metadata import EntryPoint


@pytest.fixture()
def pathlib_monkey_patch(request):
    load_pathlib_monkey_patch()
    request.addfinalizer(unload_pathlib_monkey_patch)


@pytest.fixture()
def mock_entry_points_path(monkeypatch):
    def mock_entry_points(*args, **kwargs):
        return [
            EntryPoint(
                group="uri_pathlib_backend",
                name="test",
                value="tests.pathlib_test_uri_backend:register_uri_pathlib_backend",
            ),
            EntryPoint(
                group="uri_pathlib_backend",
                name="test2",
                value=(
                    "tests.pathlib_test_uri_backend:"
                    "register_uri_pathlib_backend_test2"
                ),
            ),
        ]

    monkeypatch.setattr("uri_pathlib_factory.main.entry_points", mock_entry_points)


@pytest.fixture()
def reloaded_plugin_registry_with_test_plugin(mock_entry_points_path):
    load_uri_backends_from_plugins()
