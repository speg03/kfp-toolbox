import os
from typing import Dict, List

import pytest
from kfp import compiler as compiler_v1
from kfp import dsl as dsl_v1
from kfp.v2 import compiler, dsl

from kfp_toolbox.pipeline_parser import Parameter, parse_pipeline_package


class TestParsePipelinePackage:
    def test_v1(self, tmp_path):
        @dsl.component()
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
        compiler_v1.Compiler(mode=dsl_v1.PipelineExecutionMode.V2_COMPATIBLE).compile(
            pipeline_func=echo_pipeline, package_path=pipeline_path
        )
        pipeline = parse_pipeline_package(pipeline_path)

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

    def test(self, tmp_path):
        @dsl.component()
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
        compiler.Compiler().compile(
            pipeline_func=echo_pipeline, package_path=pipeline_path
        )
        pipeline = parse_pipeline_package(pipeline_path)

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

    def test_falsy_default_values_v1(self, tmp_path):
        @dsl.component()
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
        compiler_v1.Compiler(mode=dsl_v1.PipelineExecutionMode.V2_COMPATIBLE).compile(
            pipeline_func=echo_pipeline, package_path=pipeline_path
        )
        pipeline = parse_pipeline_package(pipeline_path)

        int_param = Parameter(name="int_param", type=int, default=0)
        float_param = Parameter(name="float_param", type=float, default=0.0)
        str_param = Parameter(name="str_param", type=str, default="")

        assert pipeline.name == "echo-pipeline"
        assert len(pipeline.parameters) == 3
        assert int_param in pipeline.parameters
        assert float_param in pipeline.parameters
        assert str_param in pipeline.parameters

    def test_falsy_default_values(self, tmp_path):
        @dsl.component()
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
        compiler.Compiler().compile(
            pipeline_func=echo_pipeline, package_path=pipeline_path
        )
        pipeline = parse_pipeline_package(pipeline_path)

        int_param = Parameter(name="int_param", type=int, default=0)
        float_param = Parameter(name="float_param", type=float, default=0.0)
        str_param = Parameter(name="str_param", type=str, default="")

        assert pipeline.name == "echo-pipeline"
        assert len(pipeline.parameters) == 3
        assert int_param in pipeline.parameters
        assert float_param in pipeline.parameters
        assert str_param in pipeline.parameters

    def test_no_parameters_v1(self, tmp_path):
        @dsl.component()
        def echo() -> str:
            return "hello, world"

        @dsl.pipeline(name="echo-pipeline")
        def echo_pipeline():
            echo()

        pipeline_path = os.fspath(tmp_path / "pipeline.yaml")
        compiler_v1.Compiler(mode=dsl_v1.PipelineExecutionMode.V2_COMPATIBLE).compile(
            pipeline_func=echo_pipeline, package_path=pipeline_path
        )

        pipeline = parse_pipeline_package(pipeline_path)
        assert pipeline.name == "echo-pipeline"
        assert len(pipeline.parameters) == 0

    def test_no_parameters(self, tmp_path):
        @dsl.component()
        def echo() -> str:
            return "hello, world"

        @dsl.pipeline(name="echo-pipeline")
        def echo_pipeline():
            echo()

        pipeline_path = os.fspath(tmp_path / "pipeline.json")
        compiler.Compiler().compile(
            pipeline_func=echo_pipeline, package_path=pipeline_path
        )

        pipeline = parse_pipeline_package(pipeline_path)
        assert pipeline.name == "echo-pipeline"
        assert len(pipeline.parameters) == 0

    def test_empty_file(self, tmp_path):
        pipeline = ""
        pipeline_path = os.fspath(tmp_path / "pipeline.json")
        with open(pipeline_path, "w") as f:
            f.write(pipeline)

        with pytest.raises(ValueError) as exc_info:
            parse_pipeline_package(pipeline_path)

        assert str(exc_info.value) == f"invalid schema: {pipeline_path}"

    def test_invalid_schema(self, tmp_path):
        pipeline = """
            {
                "invalid_schema": {}
            }
        """
        pipeline_path = os.fspath(tmp_path / "pipeline.json")
        with open(pipeline_path, "w") as f:
            f.write(pipeline)

        with pytest.raises(ValueError) as exc_info:
            parse_pipeline_package(pipeline_path)

        assert str(exc_info.value) == f"invalid schema: {pipeline_path}"
