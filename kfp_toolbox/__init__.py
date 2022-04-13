from .decorators import spec  # noqa: F401

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version  # type: ignore

__version__ = version("kfp-toolbox")
