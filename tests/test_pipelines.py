import os
from typing import Dict, List

import pytest
from kfp.v2 import compiler, dsl

from kfp_toolbox.pipelines import Parameter, load_pipeline_from_file


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
    assert pipeline.name == "echo-pipeline"
    assert len(pipeline.parameters) == 7
    assert Parameter(name="no_default_param", type=int) in pipeline.parameters
    assert Parameter(name="int_param", type=int, default=1) in pipeline.parameters
    assert Parameter(name="float_param", type=float, default=1.5) in pipeline.parameters
    assert (
        Parameter(name="str_param", type=str, default="string_value")
        in pipeline.parameters
    )
    assert Parameter(name="bool_param", type=str, default="True") in pipeline.parameters
    assert (
        Parameter(name="list_param", type=str, default="[1, 2, 3]")
        in pipeline.parameters
    )
    assert (
        Parameter(name="dict_param", type=str, default='{"key": 4}')
        in pipeline.parameters
    )


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
