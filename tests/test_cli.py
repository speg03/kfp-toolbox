import os
from pathlib import PosixPath
from unittest.mock import patch

from kfp.v2 import compiler, dsl
from typer.testing import CliRunner

from kfp_toolbox.cli import app

runner = CliRunner()


@patch("kfp_toolbox.pipelines.submit_pipeline_job")
def test_submit(mock_submit_pipeline_job, tmp_path):
    @dsl.component()
    def echo() -> str:
        return "hello, world"

    @dsl.pipeline(name="echo-pipeline")
    def echo_pipeline(param: int = 1, weird_param__: str = "default_string"):
        echo()

    pipeline_path = os.fspath(tmp_path / "pipeline.json")
    compiler.Compiler().compile(pipeline_func=echo_pipeline, package_path=pipeline_path)

    result = runner.invoke(
        app,
        [
            "submit",
            f"--pipeline-file={pipeline_path}",
            "--endpoint=http://localhost:8080",
            "--label=project:hello",
            "--label=test:true",
            "--",
            "--param=5",
            "--weird-param=passed_value",
        ],
    )

    assert result.exit_code == 0
    mock_submit_pipeline_job.assert_called_once_with(
        pipeline_file=PosixPath(pipeline_path),
        endpoint="http://localhost:8080",
        iap_client_id=None,
        api_namespace="kubeflow",
        other_client_id=None,
        other_client_secret=None,
        arguments={"param": 5, "weird_param__": "passed_value"},
        run_name=None,
        experiment_name=None,
        namespace=None,
        pipeline_root=None,
        enable_caching=None,
        service_account=None,
        encryption_spec_key_name=None,
        labels={"project": "hello", "test": "true"},
        project=None,
        location=None,
        network=None,
    )


@patch("kfp_toolbox.pipelines.submit_pipeline_job")
def test_submit_with_caching(mock_submit_pipeline_job, tmp_path):
    @dsl.component()
    def echo() -> str:
        return "hello, world"

    @dsl.pipeline(name="echo-pipeline")
    def echo_pipeline():
        echo()

    pipeline_path = os.fspath(tmp_path / "pipeline.json")
    compiler.Compiler().compile(pipeline_func=echo_pipeline, package_path=pipeline_path)

    result = runner.invoke(
        app, ["submit", f"--pipeline-file={pipeline_path}", "--caching"]
    )

    assert result.exit_code == 0
    mock_submit_pipeline_job.assert_called_once_with(
        pipeline_file=PosixPath(pipeline_path),
        endpoint=None,
        iap_client_id=None,
        api_namespace="kubeflow",
        other_client_id=None,
        other_client_secret=None,
        arguments={},
        run_name=None,
        experiment_name=None,
        namespace=None,
        pipeline_root=None,
        enable_caching=True,
        service_account=None,
        encryption_spec_key_name=None,
        labels={},
        project=None,
        location=None,
        network=None,
    )


@patch("kfp_toolbox.pipelines.submit_pipeline_job")
def test_submit_with_no_caching(mock_submit_pipeline_job, tmp_path):
    @dsl.component()
    def echo() -> str:
        return "hello, world"

    @dsl.pipeline(name="echo-pipeline")
    def echo_pipeline():
        echo()

    pipeline_path = os.fspath(tmp_path / "pipeline.json")
    compiler.Compiler().compile(pipeline_func=echo_pipeline, package_path=pipeline_path)

    result = runner.invoke(
        app, ["submit", f"--pipeline-file={pipeline_path}", "--no-caching"]
    )

    assert result.exit_code == 0
    mock_submit_pipeline_job.assert_called_once_with(
        pipeline_file=PosixPath(pipeline_path),
        endpoint=None,
        iap_client_id=None,
        api_namespace="kubeflow",
        other_client_id=None,
        other_client_secret=None,
        arguments={},
        run_name=None,
        experiment_name=None,
        namespace=None,
        pipeline_root=None,
        enable_caching=False,
        service_account=None,
        encryption_spec_key_name=None,
        labels={},
        project=None,
        location=None,
        network=None,
    )


def test_submit_with_no_pipelie_files():
    result = runner.invoke(app, ["submit"])

    assert result.exit_code != 0
    assert "Error: The --pipeline-file option must be specified." in result.output


def test_submit_with_invalid_label(tmp_path):
    @dsl.component()
    def echo() -> str:
        return "hello, world"

    @dsl.pipeline(name="echo-pipeline")
    def echo_pipeline():
        echo()

    pipeline_path = os.fspath(tmp_path / "pipeline.json")
    compiler.Compiler().compile(pipeline_func=echo_pipeline, package_path=pipeline_path)

    result = runner.invoke(
        app, ["submit", f"--pipeline-file={pipeline_path}", "--label=invalid_label"]
    )

    assert result.exit_code != 0
    assert (
        "Error: The --label value must be contained a colon.: invalid_label"
        in result.output
    )


def test_submit_help():
    result = runner.invoke(app, ["submit", "--help"])

    assert result.exit_code == 0
    assert result.output.startswith("Usage: ")


def test_main():
    result = runner.invoke(app)

    assert result.exit_code != 0
    assert result.output.startswith("Usage: ")


def test_main_help():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert result.output.startswith("Usage: ")


def test_main_version():
    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert "version" in result.output
