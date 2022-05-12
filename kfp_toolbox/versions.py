try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version  # type: ignore

kfp_toolbox_version = version("kfp-toolbox")
kfp_version = version("kfp")
