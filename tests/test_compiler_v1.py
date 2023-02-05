import json
import os
import pathlib
import sys

import pytest
import yaml
from kfp_toolbox import compiler


class TestCompilePipelineFunctionFromFile:
    @pytest.fixture(autouse=True)
    def delete_imported_pipeline_modules(self):
        if "single_pipeline" in sys.modules:
            del sys.modules["single_pipeline"]

    def test_compile_pipeline(self, tmp_path: pathlib.Path) -> None:
        package_path = os.fspath(tmp_path / "pipeline.yaml")
        compiler.compile_pipeline_function(
            package_path=package_path,
            pyfile="./src/kfp_toolbox_testing/pipelines/single_pipeline.py",
            function_name="echo_pipeline",
            legacy_mode="V1_LEGACY",
        )

        assert os.path.isfile(package_path)
        with open(package_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)
        spec_json = json.loads(
            pipeline_spec["metadata"]["annotations"][
                "pipelines.kubeflow.org/pipeline_spec"
            ]
        )
        assert spec_json["name"] == "echo-pipeline"

    def test_compile_pipeline_in_v2_compatible_mode(
        self, tmp_path: pathlib.Path
    ) -> None:
        package_path = os.fspath(tmp_path / "pipeline.yaml")
        compiler.compile_pipeline_function(
            package_path=package_path,
            pyfile="./src/kfp_toolbox_testing/pipelines/single_pipeline.py",
            function_name="echo_pipeline",
            legacy_mode="V2_COMPATIBLE",
        )

        assert os.path.isfile(package_path)
        with open(package_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)
        spec_json = json.loads(
            pipeline_spec["metadata"]["annotations"][
                "pipelines.kubeflow.org/pipeline_spec"
            ]
        )
        assert spec_json["name"] == "echo-pipeline"

    def test_compile_pipeline_in_v2_engine_mode(self, tmp_path: pathlib.Path) -> None:
        package_path = os.fspath(tmp_path / "pipeline.yaml")
        with pytest.raises(ValueError) as exc_info:
            compiler.compile_pipeline_function(
                package_path=package_path,
                pyfile="./src/kfp_toolbox_testing/pipelines/single_pipeline.py",
                function_name="echo_pipeline",
                legacy_mode="V2_ENGINE",
            )
        assert str(exc_info.value) == "V2_ENGINE execution mode is not supported yet."

    def test_compile_pipeline_in_invalid_mode(self, tmp_path: pathlib.Path) -> None:
        package_path = os.fspath(tmp_path / "pipeline.yaml")
        with pytest.raises(ValueError) as exc_info:
            compiler.compile_pipeline_function(
                package_path=package_path,
                pyfile="./src/kfp_toolbox_testing/pipelines/single_pipeline.py",
                function_name="echo_pipeline",
                legacy_mode="INVALID",
            )
        assert str(exc_info.value) == (
            "legacy_mode must be one of 'V1_LEGACY', 'V2_COMPATIBLE', or 'V2_ENGINE'."
        )


class TestCompilePipelineFunctionFromModule:
    @pytest.fixture(autouse=True)
    def delete_imported_pipeline_modules(self):
        if "kfp_toolbox_testing.pipelines.single_pipeline" in sys.modules:
            del sys.modules["kfp_toolbox_testing.pipelines.single_pipeline"]

    def test_compile_pipeline(self, tmp_path: pathlib.Path) -> None:
        package_path = os.fspath(tmp_path / "pipeline.yaml")
        compiler.compile_pipeline_function(
            package_path=package_path,
            module="kfp_toolbox_testing.pipelines.single_pipeline",
            function_name="echo_pipeline",
            legacy_mode="V1_LEGACY",
        )

        assert os.path.isfile(package_path)
        with open(package_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)
        spec_json = json.loads(
            pipeline_spec["metadata"]["annotations"][
                "pipelines.kubeflow.org/pipeline_spec"
            ]
        )
        assert spec_json["name"] == "echo-pipeline"


class TestCompilePipelineFunctionFromInvalidSource:
    def test_no_pyfile_or_module(self) -> None:
        with pytest.raises(ValueError) as exc_info:
            compiler.compile_pipeline_function(
                package_path="path/to/pipeline.yaml", legacy_mode="V1_LEGACY"
            )
        assert str(exc_info.value) == "You must specify either pyfile or module."
