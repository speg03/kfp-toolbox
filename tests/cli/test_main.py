from click.testing import CliRunner

from kfp_toolbox.cli import main


def test_main():
    runner = CliRunner()
    result = runner.invoke(main.main)

    assert result.exit_code == 0
    assert result.output.startswith("Usage: ")


def test_main_version():
    runner = CliRunner()
    result = runner.invoke(main.main, ["--version"])

    assert result.exit_code == 0
    assert "version" in result.output
