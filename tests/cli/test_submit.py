import os
from unittest.mock import patch

from click.testing import CliRunner
from kfp.v2 import compiler, dsl

from kfp_toolbox.cli import submit


@patch("kfp_toolbox.pipelines.submit_pipeline_job")
def test_submit(mock_submit_pipeline_job, tmp_path):
    @dsl.component
    def echo() -> str:
        return "hello, world"

    @dsl.pipeline(name="echo-pipeline")
    def echo_pipeline(param: int = 1, weird_param__: str = "Default String"):
        echo()

    pipeline_path = os.fspath(tmp_path / "pipeline.json")
    compiler.Compiler().compile(pipeline_func=echo_pipeline, package_path=pipeline_path)

    runner = CliRunner()
    result = runner.invoke(
        submit.submit,
        [
            "--pipeline-file",
            pipeline_path,
            "--",
            "--param",
            "5",
            "--weird-param",
            "Passed Value",
        ],
    )

    assert result.exit_code == 0
    mock_submit_pipeline_job.assert_called_once_with(
        pipeline_file=pipeline_path,
        endpoint=None,
        experiment_name=None,
        pipeline_root=None,
        arguments={"param": 5, "weird_param__": "Passed Value"},
    )


def test_submit_with_no_pipelie_files():
    runner = CliRunner()
    result = runner.invoke(submit.submit)

    assert result.exit_code != 0
    assert "Error: The --pipeline-file option must be specified." in result.output


def test_submit_help():
    runner = CliRunner()
    result = runner.invoke(submit.submit, ["--help"])

    assert result.exit_code == 0
    assert result.output.startswith("Usage: ")
