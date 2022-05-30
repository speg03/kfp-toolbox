from click.testing import CliRunner

from kfp_toolbox.cli import submit


def test_submit_help():
    runner = CliRunner()
    result = runner.invoke(submit.submit, ["--help"])

    assert result.exit_code == 0
    assert result.output.startswith("Usage: ")
