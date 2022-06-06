try:
    import importlib.metadata as metadata
except ImportError:
    import importlib_metadata as metadata  # type: ignore

kfp_toolbox_version = metadata.version("kfp-toolbox")
kfp_version = metadata.version("kfp")
google_cloud_aiplatform_version = metadata.version("google-cloud-aiplatform")
