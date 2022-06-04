import argparse
from typing import Sequence

import click

from kfp_toolbox import pipelines


@click.command(add_help_option=False)
@click.option("-h", "--help", is_flag=True, help="Show this message and exit.")
@click.option(
    "-f",
    "--pipeline-file",
    type=click.Path(exists=True, dir_okay=False),
    help="Path of the pipeline package file. (required)",
)
@click.option("--endpoint", help="Endpoint of the KFP API service to connect.")
@click.option("-e", "--experiment-name", help="Experiment name of the run.")
@click.option("--pipeline-root", help="The root path of the pipeline outputs.")
@click.argument("pipeline_parameters", nargs=-1)
@click.pass_context
def submit(
    ctx: click.Context,
    help: bool,
    pipeline_file: str,
    endpoint: str,
    experiment_name: str,
    pipeline_root: str,
    pipeline_parameters: Sequence[str],
):
    """Submit a pipeline job from the pipeline package file."""
    parser = argparse.ArgumentParser(add_help=False, usage=argparse.SUPPRESS)
    parameters_group = parser.add_argument_group("Pipeline parameters")
    if pipeline_file:
        pipeline = pipelines.load_pipeline_from_file(pipeline_file)
        for parameter in pipeline.parameters:
            sanitized_name = parameter.name.replace("_", "-").lstrip("-").rstrip("-")
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

    args = parser.parse_args(pipeline_parameters or [])
    arguments_dict = vars(args)

    pipelines.submit_pipeline_job(
        pipeline_file=pipeline_file,
        endpoint=endpoint,
        experiment_name=experiment_name,
        pipeline_root=pipeline_root,
        arguments=arguments_dict,
    )
