import click

from .. import versions
from . import submit


@click.group(commands=[submit.submit])
@click.help_option("-h", "--help")
@click.version_option(
    versions.kfp_toolbox_version,
    "-V",
    "--version",
    message=(
        "%(prog)s, version %(version)s\n"
        f"kfp, version {versions.kfp_version}\n"
        f"google-cloud-aiplatform, version {versions.google_cloud_aiplatform_version}"
    ),
)
def main():
    pass
