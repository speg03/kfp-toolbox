import os
from typing import Dict, List
from unittest.mock import patch

import pytest
from kfp import compiler as compiler_v1
from kfp.dsl import PipelineExecutionMode
from kfp.v2 import compiler, dsl

from kfp_toolbox.pipelines import (
    Parameter,
    load_pipeline_from_file,
    submit_pipeline_job,
)


def test_load_pipeline_from_file_v1(tmp_path):
    @dsl.component
    def echo() -> str:
        return "hello, world"

    @dsl.pipeline(name="echo-pipeline")
    def echo_pipeline(
        no_default_param: int,
        int_param: int = 1,
        float_param: float = 1.5,
        str_param: str = "string_value",
        bool_param: bool = True,
        list_param: List[int] = [1, 2, 3],
        dict_param: Dict[str, int] = {"key": 4},
    ):
        echo()

    pipeline_path = os.fspath(tmp_path / "pipeline.yaml")
    compiler_v1.Compiler(mode=PipelineExecutionMode.V2_COMPATIBLE).compile(
        pipeline_func=echo_pipeline, package_path=pipeline_path
    )
    pipeline = load_pipeline_from_file(pipeline_path)

    no_default_param = Parameter(name="no_default_param", type=int)
    int_param = Parameter(name="int_param", type=int, default=1)
    float_param = Parameter(name="float_param", type=float, default=1.5)
    str_param = Parameter(name="str_param", type=str, default="string_value")
    bool_param = Parameter(name="bool_param", type=str, default="True")
    list_param = Parameter(name="list_param", type=str, default="[1, 2, 3]")
    dict_param = Parameter(name="dict_param", type=str, default='{"key": 4}')

    assert pipeline.name == "echo-pipeline"
    assert len(pipeline.parameters) == 7
    assert no_default_param in pipeline.parameters
    assert int_param in pipeline.parameters
    assert float_param in pipeline.parameters
    assert str_param in pipeline.parameters
    assert bool_param in pipeline.parameters
    assert list_param in pipeline.parameters
    assert dict_param in pipeline.parameters


def test_load_pipeline_from_file(tmp_path):
    @dsl.component
    def echo() -> str:
        return "hello, world"

    @dsl.pipeline(name="echo-pipeline")
    def echo_pipeline(
        no_default_param: int,
        int_param: int = 1,
        float_param: float = 1.5,
        str_param: str = "string_value",
        bool_param: bool = True,
        list_param: List[int] = [1, 2, 3],
        dict_param: Dict[str, int] = {"key": 4},
    ):
        echo()

    pipeline_path = os.fspath(tmp_path / "pipeline.json")
    compiler.Compiler().compile(pipeline_func=echo_pipeline, package_path=pipeline_path)
    pipeline = load_pipeline_from_file(pipeline_path)

    no_default_param = Parameter(name="no_default_param", type=int)
    int_param = Parameter(name="int_param", type=int, default=1)
    float_param = Parameter(name="float_param", type=float, default=1.5)
    str_param = Parameter(name="str_param", type=str, default="string_value")
    bool_param = Parameter(name="bool_param", type=str, default="True")
    list_param = Parameter(name="list_param", type=str, default="[1, 2, 3]")
    dict_param = Parameter(name="dict_param", type=str, default='{"key": 4}')

    assert pipeline.name == "echo-pipeline"
    assert len(pipeline.parameters) == 7
    assert no_default_param in pipeline.parameters
    assert int_param in pipeline.parameters
    assert float_param in pipeline.parameters
    assert str_param in pipeline.parameters
    assert bool_param in pipeline.parameters
    assert list_param in pipeline.parameters
    assert dict_param in pipeline.parameters


def test_load_pipeline_from_file_v1_with_falsy_default_values(tmp_path):
    @dsl.component
    def echo() -> str:
        return "hello, world"

    @dsl.pipeline(name="echo-pipeline")
    def echo_pipeline(
        int_param: int = 0,
        float_param: float = 0.0,
        str_param: str = "",
    ):
        echo()

    pipeline_path = os.fspath(tmp_path / "pipeline.yaml")
    compiler_v1.Compiler(mode=PipelineExecutionMode.V2_COMPATIBLE).compile(
        pipeline_func=echo_pipeline, package_path=pipeline_path
    )
    pipeline = load_pipeline_from_file(pipeline_path)

    int_param = Parameter(name="int_param", type=int, default=0)
    float_param = Parameter(name="float_param", type=float, default=0.0)
    str_param = Parameter(name="str_param", type=str, default="")

    assert pipeline.name == "echo-pipeline"
    assert len(pipeline.parameters) == 3
    assert int_param in pipeline.parameters
    assert float_param in pipeline.parameters
    assert str_param in pipeline.parameters


def test_load_pipeline_from_file_with_falsy_default_values(tmp_path):
    @dsl.component
    def echo() -> str:
        return "hello, world"

    @dsl.pipeline(name="echo-pipeline")
    def echo_pipeline(
        int_param: int = 0,
        float_param: float = 0.0,
        str_param: str = "",
    ):
        echo()

    pipeline_path = os.fspath(tmp_path / "pipeline.json")
    compiler.Compiler().compile(pipeline_func=echo_pipeline, package_path=pipeline_path)
    pipeline = load_pipeline_from_file(pipeline_path)

    int_param = Parameter(name="int_param", type=int, default=0)
    float_param = Parameter(name="float_param", type=float, default=0.0)
    str_param = Parameter(name="str_param", type=str, default="")

    assert pipeline.name == "echo-pipeline"
    assert len(pipeline.parameters) == 3
    assert int_param in pipeline.parameters
    assert float_param in pipeline.parameters
    assert str_param in pipeline.parameters


def test_load_pipeline_from_file_v1_with_no_parameters(tmp_path):
    @dsl.component
    def echo() -> str:
        return "hello, world"

    @dsl.pipeline(name="echo-pipeline")
    def echo_pipeline():
        echo()

    pipeline_path = os.fspath(tmp_path / "pipeline.yaml")
    compiler_v1.Compiler(mode=PipelineExecutionMode.V2_COMPATIBLE).compile(
        pipeline_func=echo_pipeline, package_path=pipeline_path
    )

    pipeline = load_pipeline_from_file(pipeline_path)
    assert pipeline.name == "echo-pipeline"
    assert len(pipeline.parameters) == 0


def test_load_pipeline_from_file_with_no_parameters(tmp_path):
    @dsl.component
    def echo() -> str:
        return "hello, world"

    @dsl.pipeline(name="echo-pipeline")
    def echo_pipeline():
        echo()

    pipeline_path = os.fspath(tmp_path / "pipeline.json")
    compiler.Compiler().compile(pipeline_func=echo_pipeline, package_path=pipeline_path)

    pipeline = load_pipeline_from_file(pipeline_path)
    assert pipeline.name == "echo-pipeline"
    assert len(pipeline.parameters) == 0


def test_load_pipeline_from_file_with_invalid_schema(tmp_path):
    pipeline = """
        {
            "invalid_schema": {}
        }
    """
    pipeline_path = os.fspath(tmp_path / "pipeline.json")
    with open(pipeline_path, "w") as f:
        f.write(pipeline)

    with pytest.raises(ValueError) as exc_info:
        load_pipeline_from_file(pipeline_path)

    assert str(exc_info.value) == f"invalid schema: {pipeline_path}"


@patch("google.cloud.aiplatform.PipelineJob")
@patch("kfp.Client")
def test_submit_pipeline_job(mock_kfp, mock_aip):
    submit_pipeline_job(
        pipeline_file="/path/to/file", arguments={"param": 1}, run_name="test-run"
    )

    mock_kfp.assert_not_called()
    mock_aip.assert_called_once_with(
        display_name=None,
        template_path="/path/to/file",
        job_id="test-run",
        pipeline_root=None,
        parameter_values={"param": 1},
        enable_caching=None,
        encryption_spec_key_name=None,
        labels=None,
        credentials=None,
        project=None,
        location=None,
    )
    mock_aip.return_value.submit.assert_called_once_with()


@patch("google.cloud.aiplatform.PipelineJob")
@patch("kfp.Client")
def test_submit_pipeline_job_with_endpoint(mock_kfp, mock_aip):
    submit_pipeline_job(
        pipeline_file="/path/to/file",
        arguments={"param": 1},
        run_name="test-run",
        endpoint="http://localhost:8080",
    )

    mock_aip.assert_not_called()
    mock_kfp.assert_called_once_with(host="http://localhost:8080")
    mock_kfp.return_value.create_run_from_pipeline_package.assert_called_once_with(
        pipeline_file="/path/to/file",
        arguments={"param": 1},
        run_name="test-run",
        experiment_name=None,
        namespace=None,
        pipeline_root=None,
        enable_caching=None,
        service_account=None,
    )
