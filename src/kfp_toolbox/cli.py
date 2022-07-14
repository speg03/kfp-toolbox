import argparse
from typing import Optional, Sequence

import click

from . import pipelines, versions


@click.command(add_help_option=False)
@click.option("-h", "--help", is_flag=True, help="Show this message and exit.")
@click.option(
    "-f",
    "--pipeline-file",
    type=click.Path(exists=True, dir_okay=False),
    help="Path of the pipeline package file. (required)",
)
@click.option("--endpoint", help="Endpoint of the KFP API service to connect.")
@click.option("--iap-client-id")
@click.option("--api-namespace", default="kubeflow")
@click.option("--other-client-id")
@click.option("--other-client-secret")
@click.option("--run-name")
@click.option("-e", "--experiment-name", help="Experiment name of the run.")
@click.option("-n", "--namespace")
@click.option("--pipeline-root", help="The root path of the pipeline outputs.")
@click.option("--disable-caching", "enable_caching", is_flag=True, default=True)
@click.option("--service-account")
@click.option("--encryption-spec-key-name")
@click.option("-l", "--label", "labels", multiple=True)
@click.option("--project")
@click.option("--location")
@click.option("--network")
@click.argument("pipeline_parameters", nargs=-1)
@click.pass_context
def submit(
    ctx: click.Context,
    help: bool,
    pipeline_file: Optional[str],
    endpoint: Optional[str],
    iap_client_id: Optional[str],
    api_namespace: str,
    other_client_id: Optional[str],
    other_client_secret: Optional[str],
    run_name: Optional[str],
    experiment_name: Optional[str],
    namespace: Optional[str],
    pipeline_root: Optional[str],
    enable_caching: bool,
    service_account: Optional[str],
    encryption_spec_key_name: Optional[str],
    labels: Optional[Sequence[str]],
    project: Optional[str],
    location: Optional[str],
    network: Optional[str],
    pipeline_parameters: Optional[Sequence[str]],
):
    """Submit a pipeline job from the pipeline package file."""
    parser = argparse.ArgumentParser(add_help=False, usage=argparse.SUPPRESS)
    parameters_group = parser.add_argument_group("Pipeline parameters")
    if pipeline_file:
        pipeline = pipelines.load_pipeline_from_file(pipeline_file)
        for parameter in pipeline.parameters:
            sanitized_name = parameter.name.replace("_", "-").strip("-")
            required = parameter.default is None
            parameters_group.add_argument(
                f"--{sanitized_name}",
                type=parameter.type,
                default=parameter.default,
                dest=parameter.name,
                help="(required)" if required else "default: %(default)s",
                required=required,
            )

    if help:
        print(ctx.get_help())
        print()
        parser.print_help()
        ctx.exit(0)
    elif not pipeline_file:
        ctx.fail("The --pipeline-file option must be specified.")

    labels_dict = {}
    for label in labels or []:
        try:
            key, value = label.split(":", maxsplit=1)
        except ValueError:
            ctx.fail(f"The --label value must be contained a colon.: {label}")
        labels_dict[key] = value

    args = parser.parse_args(pipeline_parameters or [])
    arguments_dict = vars(args)

    pipelines.submit_pipeline_job(
        pipeline_file=pipeline_file,  # type: ignore
        endpoint=endpoint,
        iap_client_id=iap_client_id,
        api_namespace=api_namespace,
        other_client_id=other_client_id,
        other_client_secret=other_client_secret,
        arguments=arguments_dict,
        run_name=run_name,
        experiment_name=experiment_name,
        namespace=namespace,
        pipeline_root=pipeline_root,
        enable_caching=enable_caching,
        service_account=service_account,
        encryption_spec_key_name=encryption_spec_key_name,
        labels=labels_dict,
        project=project,
        location=location,
        network=network,
    )


@click.group(commands=[submit])
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
    pass  # pragma: no cover
