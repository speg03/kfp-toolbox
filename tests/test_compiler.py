import os
import pathlib
import sys

import pytest
import yaml
from kfp_toolbox import compiler


class TestCompilePipelineFunctionFromFile:
    @pytest.fixture(autouse=True)
    def delete_imported_pipeline_modules(self):
        module_name = "single_pipeline"
        if module_name in sys.modules:
            del sys.modules[module_name]

    def test_compile_pipeline(self, tmp_path: pathlib.Path) -> None:
        package_path = os.fspath(tmp_path / "pipeline.json")
        compiler.compile_pipeline_function(
            package_path=package_path,
            pyfile="./src/kfp_toolbox_testing/pipelines/single_pipeline.py",
            function_name="echo_pipeline",
        )

        assert os.path.isfile(package_path)
        with open(package_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)
        assert pipeline_spec["pipelineSpec"]["pipelineInfo"]["name"] == "echo-pipeline"

    def test_compile_pipeline_with_no_function_name(
        self, tmp_path: pathlib.Path
    ) -> None:
        package_path = os.fspath(tmp_path / "pipeline.json")
        compiler.compile_pipeline_function(
            package_path=package_path,
            pyfile="./src/kfp_toolbox_testing/pipelines/single_pipeline.py",
        )

        assert os.path.isfile(package_path)
        with open(package_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)
        assert pipeline_spec["pipelineSpec"]["pipelineInfo"]["name"] == "echo-pipeline"


class TestCompilePipelineFunctionFromModule:
    @pytest.fixture(autouse=True)
    def delete_imported_pipeline_modules(self):
        module_name = "kfp_toolbox_testing.pipelines.single_pipeline"
        if module_name in sys.modules:
            del sys.modules[module_name]

    def test_compile_pipeline(self, tmp_path: pathlib.Path) -> None:
        package_path = os.fspath(tmp_path / "pipeline.json")
        compiler.compile_pipeline_function(
            package_path=package_path,
            module="kfp_toolbox_testing.pipelines.single_pipeline",
            function_name="echo_pipeline",
        )

        assert os.path.isfile(package_path)
        with open(package_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)
        assert pipeline_spec["pipelineSpec"]["pipelineInfo"]["name"] == "echo-pipeline"

    def test_compile_pipeline_with_no_function_name(
        self, tmp_path: pathlib.Path
    ) -> None:
        package_path = os.fspath(tmp_path / "pipeline.json")
        compiler.compile_pipeline_function(
            package_path=package_path,
            module="kfp_toolbox_testing.pipelines.single_pipeline",
        )

        assert os.path.isfile(package_path)
        with open(package_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)
        assert pipeline_spec["pipelineSpec"]["pipelineInfo"]["name"] == "echo-pipeline"

    def test_invalid_pipeline_function_name_in_module(self):
        with pytest.raises(ValueError) as exc_info:
            compiler.compile_pipeline_function(
                package_path="path/to/pipeline.json",
                module="kfp_toolbox_testing.pipelines.single_pipeline",
                function_name="invalid_pipeline",
            )
        assert str(exc_info.value) == (
            "'kfp_toolbox_testing.pipelines.single_pipeline' module"
            " has no function 'invalid_pipeline'."
        )

    def test_no_pipeline_functions_in_module(self):
        with pytest.raises(ValueError) as exc_info:
            compiler.compile_pipeline_function(
                package_path="path/to/pipeline.json", module="kfp_toolbox_testing"
            )
        assert str(exc_info.value) == (
            "There are no pipeline functions in the 'kfp_toolbox_testing' module."
            " Otherwise, have you already imported 'kfp_toolbox_testing'?"
        )


class TestCompilePipelineFunctionFromInvalidSource:
    def test_no_pyfile_or_module(self) -> None:
        with pytest.raises(ValueError) as exc_info:
            compiler.compile_pipeline_function(package_path="path/to/pipeline.json")
        assert str(exc_info.value) == "You must specify either pyfile or module."
