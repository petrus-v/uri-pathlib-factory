from pathlib import Path, PurePath, _PosixFlavour


class _TestFlavour(_PosixFlavour):

    is_supported = True

    def make_uri(self, path):
        uri = super().make_uri(path)
        return uri.replace("file://", "test://")


_test_flavour = _TestFlavour()


class PureTestPath(PurePath):
    """Test class purpose"""

    _flavour = _test_flavour
    __slots__ = ()


class TestPath(Path, PureTestPath):
    __slots__ = ()


def register_uri_pathlib_backend():
    """Register test:// pathlib implementation

    return a tuple with
    (scheme, PurePathClass, PathClass, Optional[params_adapter], )
    """
    scheme = "test"

    def params_adapter(cls, parsed_uri, *args, **kwargs):
        largs = list(args)
        # remove scheme and scheme separator `:`
        largs[0] = "/extra" + largs[0][len(parsed_uri.scheme) + 1 :]

        args = tuple(largs)
        return args, kwargs

    return (scheme, PureTestPath, TestPath, params_adapter)


def register_uri_pathlib_backend_test2():
    """Register test2:// pathlib implementation

    Same as test:// but using default_params_adapter

    return a tuple with
    (scheme, PurePathClass, PathClass, Optional[params_adapter], )
    """
    scheme = "test2"

    return (scheme, PureTestPath, TestPath, None)
