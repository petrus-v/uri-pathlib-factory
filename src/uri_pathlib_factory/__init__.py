import os

from .main import (
    PathFactory,
    PurePathFactory,
    load_pathlib_monkey_patch,
    load_uri_backends_from_plugins,
)

__version__ = "0.1.1"

__all__ = [
    "load_pathlib_monkey_patch",
    "PurePathFactory",
    "PathFactory",
]


load_uri_backends_from_plugins()

if os.environ.get("URI_PATHLIB_FACTORY_LOAD_PATHLIB_PATCH", "").lower() in [
    "1",
    "true",
    "on",
]:
    load_pathlib_monkey_patch()
