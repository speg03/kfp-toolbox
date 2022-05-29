try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version  # type: ignore

kfp_toolbox_version = version("kfp-toolbox")
kfp_version = version("kfp")
google_cloud_aiplatform_version = version("google-cloud-aiplatform")


def version_string() -> str:
    return (
        f"kfp-toolbox version {kfp_toolbox_version}\n"
        f"kfp version {kfp_version}\n"
        f"google-cloud-aiplatform version {google_cloud_aiplatform_version}"
    )
