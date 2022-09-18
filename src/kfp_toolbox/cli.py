import argparse
from pathlib import Path
from typing import List, Optional

import typer

from . import __version__, pipelines

app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]})


def _version_callback(version: bool):
    if version:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def callback(
    version: bool = typer.Option(
        False,
        "-V",
        "--version",
        help="Show the version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
):
    pass


@app.command(add_help_option=False)
def submit(
    ctx: typer.Context,
    help: bool = typer.Option(
        False, "-h", "--help", help="Show this message and exit."
    ),
    pipeline_file: Optional[Path] = typer.Option(
        None,
        "-f",
        "--pipeline-file",
        exists=True,
        dir_okay=False,
        help="Path of the pipeline package file.",
    ),
    endpoint: Optional[str] = typer.Option(
        None, help="Endpoint of the KFP API service to connect."
    ),
    iap_client_id: Optional[str] = typer.Option(None),
    api_namespace: str = typer.Option("kubeflow"),
    other_client_id: Optional[str] = typer.Option(None),
    other_client_secret: Optional[str] = typer.Option(None),
    run_name: Optional[str] = typer.Option(None),
    experiment_name: Optional[str] = typer.Option(
        None, "-e", "--experiment-name", help="Experiment name of the run."
    ),
    namespace: Optional[str] = typer.Option(None, "-n", "--namespace"),
    pipeline_root: Optional[str] = typer.Option(
        None, help="The root path of the pipeline outputs."
    ),
    caching: Optional[bool] = typer.Option(None),
    service_account: Optional[str] = typer.Option(None),
    encryption_spec_key_name: Optional[str] = typer.Option(None),
    labels: Optional[List[str]] = typer.Option(None, "-l", "--label"),
    project: Optional[str] = typer.Option(None),
    location: Optional[str] = typer.Option(None),
    network: Optional[str] = typer.Option(None),
    pipeline_parameters: Optional[List[str]] = typer.Argument(None),
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
                help="[required]" if required else "[default: %(default)s]",
                required=required,
            )

    if help:
        typer.echo(ctx.get_help())
        typer.echo()
        parser.print_help()
        raise typer.Exit()
    elif pipeline_file is None:
        typer.echo("Error: The --pipeline-file option must be specified.", err=True)
        raise typer.Abort()

    labels_dict = {}
    for label in labels or []:
        try:
            key, value = label.split(":", maxsplit=1)
        except ValueError:
            typer.echo(
                f"Error: The --label value must be contained a colon.: {label}",
                err=True,
            )
            raise typer.Abort()
        labels_dict[key] = value

    args = parser.parse_args(pipeline_parameters or [])
    arguments_dict = vars(args)

    pipelines.submit_pipeline_job(
        pipeline_file=pipeline_file,
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
        enable_caching=caching,
        service_account=service_account,
        encryption_spec_key_name=encryption_spec_key_name,
        labels=labels_dict,
        project=project,
        location=location,
        network=network,
    )
