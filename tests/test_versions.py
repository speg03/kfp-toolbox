from kfp_toolbox import __version__
from kfp_toolbox.versions import kfp_toolbox_version, kfp_version


def test_versions():
    assert kfp_toolbox_version
    assert kfp_version
    assert kfp_toolbox_version == __version__
