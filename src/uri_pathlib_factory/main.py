import sys
from pathlib import Path, PurePath
from urllib.parse import ParseResult, urlparse

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points

import logging

logger = logging.getLogger(__name__)

uri_backend_registry = {}


def default_params_adapter(cls, parsed_uri: ParseResult, *args, **kwargs):
    """Provide a way to backend to alter provide params

    By default remove scheme as it should not be part of the
    first params this let change params before calling __new__.

    Adapter is the same for PurePath and Path so the first
    params is the class that is going to be instantiate

    parsed_uri is ParseResult joining args with "/"

    Plugin should return args and kwargs as it will be given
    while calling PluginBackendPath(*args, **kwargs) constructor.
    """
    largs = list(args)
    # remove scheme and scheme separator `:`
    largs[0] = largs[0][len(parsed_uri.scheme) + 1 :]
    largs[0] = largs[0].replace("///", "/", 1)
    largs[0] = largs[0].replace("//", "/", 1)
    args = tuple(largs)

    return args, kwargs


def load_uri_backends_from_plugins():
    """Load or Re-Load uri_pathlib_backend plugins"""
    global uri_backend_registry
    uri_backend_registry = {}

    for plugin_register in entry_points(group="uri_pathlib_backend"):
        scheme, PurePathClass, PathClass, params_adapter = plugin_register.load()()
        uri_backend_registry[scheme] = {
            "purepath": PurePathClass,
            "path": PathClass,
            "params_adapter": params_adapter
            if params_adapter
            else default_params_adapter,
        }


def pathlib_factory_and_sanitize_args(cls, *args, **kwargs):
    """Determine if path provide to the constructor starts
    with a scheme, if it's valid scheme uri, try to find a plugin
    implementing this uri scheme pathlib backend. If found return
    the class to implement and arrange parameters to remove scheme
    from former parameter.
    """
    if args and issubclass(args[0].__class__, PurePath):
        cls = args[0].__class__
    if args and cls is Path or cls is PurePath:
        parsed_uri = urlparse("/".join(args))
        uri_backend = uri_backend_registry.get(parsed_uri.scheme, None)
        if uri_backend:
            cls = uri_backend[cls.__name__.lower()]
            args, kwargs = uri_backend["params_adapter"](
                cls, parsed_uri, *args, **kwargs
            )

    return cls, args, kwargs


class PurePathFactory:
    def __new__(cls, *args, **kwargs):
        cls, args, kwargs = pathlib_factory_and_sanitize_args(PurePath, *args, **kwargs)
        return cls.__new__(cls, *args, **kwargs)


class PathFactory:
    def __new__(cls, *args, **kwargs):
        cls, args, kwargs = pathlib_factory_and_sanitize_args(Path, *args, **kwargs)
        return cls.__new__(cls, *args, **kwargs)


original_path_new = Path.__new__
original_purepath_new = PurePath.__new__


def load_pathlib_monkey_patch():
    """In case you want to change upstream library
    that is using pathlib interface you probably want
    to monkey patch the standard library that make
    your uri backend supported by your upstream library.

    You can call this method or set environment variable
    URI_PATHLIB_FACTORY_LOAD_PATHLIB_PATCH=1. in order
    to patch the standard library.

    Once pathlib is patched you can instantiate your Path
    object like instantiate standard lib `pathlib.Path`,
    assuming you have installed `something` uri backend:

    from uri_pathlib_factory import Path as PathFactory
    from pathlib import Path

    uri_path = "something://path/to/file"
    PathFactory(uri_path)
    <SomethingPath>
    Path(uri_path)
    <SomethingPath>
    """

    def __monkey_patch_path__new__(cls, *args, **kwargs):
        if cls is Path:
            cls, args, kwargs = pathlib_factory_and_sanitize_args(cls, *args, **kwargs)
        return original_path_new(cls, *args, **kwargs)

    def __monkey_patch_purepath__new__(cls, *args, **kwargs):
        if cls is PurePath:
            cls, args, kwargs = pathlib_factory_and_sanitize_args(cls, *args, **kwargs)
        return original_purepath_new(cls, *args, **kwargs)

    Path.__new__ = __monkey_patch_path__new__
    PurePath.__new__ = __monkey_patch_purepath__new__


def unload_pathlib_monkey_patch():
    """restore pathlib class as it
    unloading monkey patch.
    """
    Path.__new__ = original_path_new
    PurePath.__new__ = original_purepath_new


load_uri_backends_from_plugins()
