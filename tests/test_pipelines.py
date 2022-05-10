import os
from typing import Dict, List

import pytest
from kfp.v2 import compiler, dsl

from kfp_toolbox.pipelines import Parameter, extract_pipeline_parameters


def test_extract_pipeline_parameters(tmp_path):
    @dsl.component
    def echo() -> str:
        return "hello, world"

    @dsl.pipeline(name="echo-pipeline")
    def echo_pipeline(
        i: int, n: int = 0, f: float = 1.0, s: str = "value", b: bool = False
    ):
        echo()

    pipeline_path = os.fspath(tmp_path / "pipeline.json")
    compiler.Compiler().compile(pipeline_func=echo_pipeline, package_path=pipeline_path)

    parameters = extract_pipeline_parameters(pipeline_path)

    assert len(parameters) == 5
    assert parameters["i"] == Parameter(name="i", type=int, default=None)
    assert parameters["n"] == Parameter(name="n", type=int, default=0)
    assert parameters["f"] == Parameter(name="f", type=float, default=1.0)
    assert parameters["s"] == Parameter(name="s", type=str, default="value")
    assert parameters["b"] == Parameter(name="b", type=str, default="False")


def test_extract_pipeline_parameters_with_struct_parameter(tmp_path):
    @dsl.component
    def echo() -> str:
        return "hello, world"

    @dsl.pipeline(name="echo-pipeline")
    def echo_pipeline(array: List[int] = [1, 2, 3], data: Dict[str, int] = {"a": 1}):
        echo()

    pipeline_path = os.fspath(tmp_path / "pipeline.json")
    compiler.Compiler().compile(pipeline_func=echo_pipeline, package_path=pipeline_path)

    parameters = extract_pipeline_parameters(pipeline_path)

    assert len(parameters) == 2
    assert parameters["array"] == Parameter(name="array", type=str, default="[1, 2, 3]")
    assert parameters["data"] == Parameter(name="data", type=str, default='{"a": 1}')


def test_extract_pipeline_parameters_with_no_parameters(tmp_path):
    @dsl.component
    def echo() -> str:
        return "hello, world"

    @dsl.pipeline(name="echo-pipeline")
    def echo_pipeline():
        echo()

    pipeline_path = os.fspath(tmp_path / "pipeline.json")
    compiler.Compiler().compile(pipeline_func=echo_pipeline, package_path=pipeline_path)

    parameters = extract_pipeline_parameters(pipeline_path)

    assert parameters == {}


def test_extract_pipeline_parameters_with_unknown_type(tmp_path):
    pipeline = """
        {
            "pipelineSpec": {
                "root": {
                    "inputDefinitions": {
                        "parameters": {
                            "v": {
                                "type": "unknown"
                            }
                        }
                    }
                }
            },
            "runtimeConfig": {
                "parameters": {
                    "v": {
                        "stringValue": ""
                    }
                }
            }
        }
    """
    pipeline_path = os.fspath(tmp_path / "pipeline.json")
    with open(pipeline_path, "w") as f:
        f.write(pipeline)

    with pytest.raises(ValueError) as exc_info:
        extract_pipeline_parameters(pipeline_path)

    assert str(exc_info.value) == (
        "Unknown type: unknown, Expected: INT, DOUBLE or STRING"
    )


def test_extract_pipeline_parameters_with_unknown_value(tmp_path):
    pipeline = """
        {
            "pipelineSpec": {
                "root": {
                    "inputDefinitions": {
                        "parameters": {
                            "v": {
                                "type": "STRING"
                            }
                        }
                    }
                }
            },
            "runtimeConfig": {
                "parameters": {
                    "v": {
                        "unknownValue": ""
                    }
                }
            }
        }
    """
    pipeline_path = os.fspath(tmp_path / "pipeline.json")
    with open(pipeline_path, "w") as f:
        f.write(pipeline)

    with pytest.raises(ValueError) as exc_info:
        extract_pipeline_parameters(pipeline_path)

    assert str(exc_info.value) == (
        "Unknown config: {'unknownValue': ''}, "
        "Expected: intValue, doubleValue or stringValue"
    )
