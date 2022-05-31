import sys

import click

from .. import versions
from . import submit


@click.group(commands=[submit.submit], invoke_without_command=True)
@click.help_option("-h", "--help")
@click.option("-V", "--version", is_flag=True, help="Show the version and exit.")
@click.pass_context
def main(ctx: click.Context, version: bool):
    if version:
        print(versions.version_string())
        sys.exit(0)
    elif ctx.invoked_subcommand is None:
        print(ctx.get_help())
        sys.exit(0)
