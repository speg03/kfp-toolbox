from kfp_toolbox import versions


def test_versions():
    assert versions.kfp_toolbox_version
    assert versions.kfp_version
    assert versions.google_cloud_aiplatform_version


def test_version_string():
    assert versions.version_string().startswith("kfp-toolbox version ")
