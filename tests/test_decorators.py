import os

import yaml
from kfp import compiler as compiler_v1
from kfp import dsl as dsl_v1
from kfp.v2 import compiler, dsl

from kfp_toolbox.decorators import (
    caching,
    container_spec,
    display_name,
    override_docstring,
    spec,
)


class TestOverrideDocstring:
    def test_no_decorators(self):
        @dsl.component()
        def echo() -> str:
            """Say hello

            This component just says hello.

            Returns:
                str: hello
            """
            return "hello, world"

        assert echo.__doc__ == "Echo\nSay hello"

    def test_no_arguments(self):
        @override_docstring()
        @dsl.component()
        def echo() -> str:
            """Say hello

            This component just says hello.

            Returns:
                str: hello
            """
            return "hello, world"

        assert echo.__doc__ == (
            "Say hello\n\n            This component just says hello.\n\n"
            "            Returns:\n                str: hello\n            "
        )

    def test_specific_docs(self):
        @override_docstring("Just say hello component")
        @dsl.component()
        def echo() -> str:
            """Say hello

            This component just says hello.

            Returns:
                str: hello
            """
            return "hello, world"

        assert echo.__doc__ == "Just say hello component"


class TestSpec:
    def test_as_decorator_v1(self, tmp_path):
        @spec(
            name="Echo Component",
            cpu="2",
            memory="16G",
            gpu="1",
            accelerator="NVIDIA_TESLA_T4",
            caching=True,
        )
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

        with open(pipeline_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)

        task = next(
            t for t in pipeline_spec["spec"]["templates"] if t["name"] == "echo"
        )
        resource_limit = task["container"]["resources"]["limits"]
        node_selector = task["nodeSelector"]
        annotations = task["metadata"]["annotations"]
        labels = task["metadata"]["labels"]

        assert resource_limit["cpu"] == "2"
        assert resource_limit["memory"] == "16G"
        assert resource_limit["nvidia.com/gpu"] == "1"
        assert node_selector["cloud.google.com/gke-accelerator"] == "NVIDIA_TESLA_T4"
        assert (
            annotations["pipelines.kubeflow.org/task_display_name"] == "Echo Component"
        )
        assert labels["pipelines.kubeflow.org/enable_caching"] == "true"

    def test_as_decorator(self, tmp_path):
        @spec(
            name="Echo Component",
            cpu="2",
            memory="16G",
            gpu="1",
            accelerator="NVIDIA_TESLA_T4",
            caching=True,
        )
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

        with open(pipeline_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)

        container = pipeline_spec["pipelineSpec"]["deploymentSpec"]["executors"][
            "exec-echo"
        ]["container"]
        task = pipeline_spec["pipelineSpec"]["root"]["dag"]["tasks"]["echo"]

        assert container["resources"]["cpuLimit"] == 2.0
        assert container["resources"]["memoryLimit"] == 16.0
        assert container["resources"]["accelerator"]["count"] == "1"
        assert container["resources"]["accelerator"]["type"] == "NVIDIA_TESLA_T4"
        assert task["taskInfo"]["name"] == "Echo Component"
        assert task["cachingOptions"]["enableCache"] is True

    def test_as_function_v1(self, tmp_path):
        @dsl.component()
        def echo() -> str:
            return "hello, world"

        @dsl.pipeline(name="echo-pipeline")
        def echo_pipeline():
            spec(
                name="Echo Component",
                cpu="2",
                memory="16G",
                gpu="1",
                accelerator="NVIDIA_TESLA_T4",
                caching=True,
            )(echo)()

        pipeline_path = os.fspath(tmp_path / "pipeline.yaml")
        compiler_v1.Compiler(mode=dsl_v1.PipelineExecutionMode.V2_COMPATIBLE).compile(
            pipeline_func=echo_pipeline, package_path=pipeline_path
        )

        with open(pipeline_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)

        task = next(
            t for t in pipeline_spec["spec"]["templates"] if t["name"] == "echo"
        )
        resource_limit = task["container"]["resources"]["limits"]
        node_selector = task["nodeSelector"]
        annotations = task["metadata"]["annotations"]
        labels = task["metadata"]["labels"]

        assert resource_limit["cpu"] == "2"
        assert resource_limit["memory"] == "16G"
        assert resource_limit["nvidia.com/gpu"] == "1"
        assert node_selector["cloud.google.com/gke-accelerator"] == "NVIDIA_TESLA_T4"
        assert (
            annotations["pipelines.kubeflow.org/task_display_name"] == "Echo Component"
        )
        assert labels["pipelines.kubeflow.org/enable_caching"] == "true"

    def test_as_function(self, tmp_path):
        @dsl.component()
        def echo() -> str:
            return "hello, world"

        @dsl.pipeline(name="echo-pipeline")
        def echo_pipeline():
            spec(
                name="Echo Component",
                cpu="2",
                memory="16G",
                gpu="1",
                accelerator="NVIDIA_TESLA_T4",
                caching=True,
            )(echo)()

        pipeline_path = os.fspath(tmp_path / "pipeline.json")
        compiler.Compiler().compile(
            pipeline_func=echo_pipeline, package_path=pipeline_path
        )

        with open(pipeline_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)

        container = pipeline_spec["pipelineSpec"]["deploymentSpec"]["executors"][
            "exec-echo"
        ]["container"]
        task = pipeline_spec["pipelineSpec"]["root"]["dag"]["tasks"]["echo"]

        assert container["resources"]["cpuLimit"] == 2.0
        assert container["resources"]["memoryLimit"] == 16.0
        assert container["resources"]["accelerator"]["count"] == "1"
        assert container["resources"]["accelerator"]["type"] == "NVIDIA_TESLA_T4"
        assert task["taskInfo"]["name"] == "Echo Component"
        assert task["cachingOptions"]["enableCache"] is True

    def test_disable_caching_v1(self, tmp_path):
        @spec(caching=False)
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

        with open(pipeline_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)

        task = next(
            t for t in pipeline_spec["spec"]["templates"] if t["name"] == "echo"
        )
        labels = task["metadata"]["labels"]

        assert labels["pipelines.kubeflow.org/enable_caching"] == "false"

    def test_disable_caching(self, tmp_path):
        @spec(caching=False)
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

        with open(pipeline_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)

        task = pipeline_spec["pipelineSpec"]["root"]["dag"]["tasks"]["echo"]

        assert "enableCache" not in task["cachingOptions"]

    def test_multiple_decorators_v1(self, tmp_path):
        default_spec = spec(cpu="2", memory="16G")

        @spec(cpu="1")
        @default_spec
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

        with open(pipeline_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)

        task = next(
            t for t in pipeline_spec["spec"]["templates"] if t["name"] == "echo"
        )
        resource_limit = task["container"]["resources"]["limits"]

        assert resource_limit["cpu"] == "1"
        assert resource_limit["memory"] == "16G"

    def test_multiple_decorators(self, tmp_path):
        default_spec = spec(cpu="2", memory="16G")

        @spec(cpu="1")
        @default_spec
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

        with open(pipeline_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)

        container = pipeline_spec["pipelineSpec"]["deploymentSpec"]["executors"][
            "exec-echo"
        ]["container"]

        assert container["resources"]["cpuLimit"] == 1.0
        assert container["resources"]["memoryLimit"] == 16.0


class TestContainerSpec:
    def test_as_decorator_v1(self, tmp_path):
        @container_spec(
            cpu="2",
            memory="16G",
            gpu="1",
            accelerator="NVIDIA_TESLA_T4",
        )
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

        with open(pipeline_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)

        task = next(
            t for t in pipeline_spec["spec"]["templates"] if t["name"] == "echo"
        )
        resource_limit = task["container"]["resources"]["limits"]
        node_selector = task["nodeSelector"]

        assert resource_limit["cpu"] == "2"
        assert resource_limit["memory"] == "16G"
        assert resource_limit["nvidia.com/gpu"] == "1"
        assert node_selector["cloud.google.com/gke-accelerator"] == "NVIDIA_TESLA_T4"

    def test_as_decorator(self, tmp_path):
        @container_spec(
            cpu="2",
            memory="16G",
            gpu="1",
            accelerator="NVIDIA_TESLA_T4",
        )
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

        with open(pipeline_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)

        container = pipeline_spec["pipelineSpec"]["deploymentSpec"]["executors"][
            "exec-echo"
        ]["container"]

        assert container["resources"]["cpuLimit"] == 2.0
        assert container["resources"]["memoryLimit"] == 16.0
        assert container["resources"]["accelerator"]["count"] == "1"
        assert container["resources"]["accelerator"]["type"] == "NVIDIA_TESLA_T4"

    def test_as_function_v1(self, tmp_path):
        @dsl.component()
        def echo() -> str:
            return "hello, world"

        @dsl.pipeline(name="echo-pipeline")
        def echo_pipeline():
            container_spec(
                cpu="2",
                memory="16G",
                gpu="1",
                accelerator="NVIDIA_TESLA_T4",
            )(echo)()

        pipeline_path = os.fspath(tmp_path / "pipeline.yaml")
        compiler_v1.Compiler(mode=dsl_v1.PipelineExecutionMode.V2_COMPATIBLE).compile(
            pipeline_func=echo_pipeline, package_path=pipeline_path
        )

        with open(pipeline_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)

        task = next(
            t for t in pipeline_spec["spec"]["templates"] if t["name"] == "echo"
        )
        resource_limit = task["container"]["resources"]["limits"]
        node_selector = task["nodeSelector"]

        assert resource_limit["cpu"] == "2"
        assert resource_limit["memory"] == "16G"
        assert resource_limit["nvidia.com/gpu"] == "1"
        assert node_selector["cloud.google.com/gke-accelerator"] == "NVIDIA_TESLA_T4"

    def test_as_function(self, tmp_path):
        @dsl.component()
        def echo() -> str:
            return "hello, world"

        @dsl.pipeline(name="echo-pipeline")
        def echo_pipeline():
            container_spec(
                cpu="2",
                memory="16G",
                gpu="1",
                accelerator="NVIDIA_TESLA_T4",
            )(echo)()

        pipeline_path = os.fspath(tmp_path / "pipeline.json")
        compiler.Compiler().compile(
            pipeline_func=echo_pipeline, package_path=pipeline_path
        )

        with open(pipeline_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)

        container = pipeline_spec["pipelineSpec"]["deploymentSpec"]["executors"][
            "exec-echo"
        ]["container"]

        assert container["resources"]["cpuLimit"] == 2.0
        assert container["resources"]["memoryLimit"] == 16.0
        assert container["resources"]["accelerator"]["count"] == "1"
        assert container["resources"]["accelerator"]["type"] == "NVIDIA_TESLA_T4"

    def test_multiple_decorators_v1(self, tmp_path):
        default_spec = container_spec(cpu="2", memory="16G")

        @container_spec(cpu="1")
        @default_spec
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

        with open(pipeline_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)

        task = next(
            t for t in pipeline_spec["spec"]["templates"] if t["name"] == "echo"
        )
        resource_limit = task["container"]["resources"]["limits"]

        assert resource_limit["cpu"] == "1"
        assert resource_limit["memory"] == "16G"

    def test_multiple_decorators(self, tmp_path):
        default_spec = container_spec(cpu="2", memory="16G")

        @container_spec(cpu="1")
        @default_spec
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

        with open(pipeline_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)

        container = pipeline_spec["pipelineSpec"]["deploymentSpec"]["executors"][
            "exec-echo"
        ]["container"]

        assert container["resources"]["cpuLimit"] == 1.0
        assert container["resources"]["memoryLimit"] == 16.0


class TestDisplayName:
    def test_v1(self, tmp_path):
        @display_name("Echo Component")
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

        with open(pipeline_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)

        task = next(
            t for t in pipeline_spec["spec"]["templates"] if t["name"] == "echo"
        )
        annotations = task["metadata"]["annotations"]
        assert (
            annotations["pipelines.kubeflow.org/task_display_name"] == "Echo Component"
        )

    def test(self, tmp_path):
        @display_name("Echo Component")
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

        with open(pipeline_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)

        task = pipeline_spec["pipelineSpec"]["root"]["dag"]["tasks"]["echo"]
        assert task["taskInfo"]["name"] == "Echo Component"


class TestCaching:
    def test_no_caching_v1(self, tmp_path):
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

        with open(pipeline_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)

        task = next(
            t for t in pipeline_spec["spec"]["templates"] if t["name"] == "echo"
        )
        labels = task["metadata"]["labels"]

        assert labels["pipelines.kubeflow.org/enable_caching"] == "true"

    def test_no_caching(self, tmp_path):
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

        with open(pipeline_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)

        task = pipeline_spec["pipelineSpec"]["root"]["dag"]["tasks"]["echo"]

        assert task["cachingOptions"]["enableCache"] is True

    def test_enable_caching_v1(self, tmp_path):
        @caching(True)
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

        with open(pipeline_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)

        task = next(
            t for t in pipeline_spec["spec"]["templates"] if t["name"] == "echo"
        )
        labels = task["metadata"]["labels"]

        assert labels["pipelines.kubeflow.org/enable_caching"] == "true"

    def test_enable_caching(self, tmp_path):
        @caching(True)
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

        with open(pipeline_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)

        task = pipeline_spec["pipelineSpec"]["root"]["dag"]["tasks"]["echo"]

        assert task["cachingOptions"]["enableCache"] is True

    def test_disable_caching_v1(self, tmp_path):
        @caching(False)
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

        with open(pipeline_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)

        task = next(
            t for t in pipeline_spec["spec"]["templates"] if t["name"] == "echo"
        )
        labels = task["metadata"]["labels"]

        assert labels["pipelines.kubeflow.org/enable_caching"] == "false"

    def test_disable_caching(self, tmp_path):
        @caching(False)
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

        with open(pipeline_path, "r") as f:
            pipeline_spec = yaml.safe_load(f)

        task = pipeline_spec["pipelineSpec"]["root"]["dag"]["tasks"]["echo"]

        assert "enableCache" not in task["cachingOptions"]
