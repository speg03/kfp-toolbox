"""Versions of the installed libraries.

This module defines versions of the installed libraries.

Attributes:
    kfp_toolbox_version: Installed version string of kfp-toolbox
    kfp_version: Installed version string of kfp
    google_cloud_aiplatform_version: Installed version string of google-cloud-aiplatform

"""

try:
    import importlib.metadata as metadata
except ImportError:
    import importlib_metadata as metadata  # type: ignore

kfp_toolbox_version: str = metadata.version("kfp-toolbox")
kfp_version: str = metadata.version("kfp")
google_cloud_aiplatform_version: str = metadata.version("google-cloud-aiplatform")
