import sys

import click


@click.command(add_help_option=False)
@click.option("-h", "--help", is_flag=True, help="Show this message and exit.")
@click.option(
    "-f",
    "--pipeline-file",
    type=click.Path(exists=True, dir_okay=False),
    help="Path of the pipeline package file.",
)
@click.pass_context
def submit(ctx: click.Context, help: bool, pipeline_file: str):
    if help:
        print(ctx.get_help())
        sys.exit(0)

    click.echo(pipeline_file)
