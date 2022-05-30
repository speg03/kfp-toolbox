import io
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from kfp_toolbox.cli import main


@patch("sys.argv", ["kfp-toolbox"])
@patch("sys.stdout", new_callable=io.StringIO)
def test_main(mock_stdout):
    with pytest.raises(SystemExit):
        main.main()

    assert mock_stdout.getvalue().startswith("Usage: ")


def test_cli():
    runner = CliRunner()
    result = runner.invoke(main.cli)

    assert result.exit_code == 0
    assert result.output.startswith("Usage: ")


def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(main.cli, ["--version"])

    assert result.exit_code == 0
    assert result.output.startswith("kfp-toolbox version ")
