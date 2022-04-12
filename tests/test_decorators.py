import json
import os

from kfp.v2 import compiler, dsl

from kfp_toolbox import spec


def test_spec_as_decorator(tmp_path):
    @spec(
        name="Echo Component",
        cpu="2",
        memory="16G",
        gpu="1",
        accelerator="NVIDIA_TESLA_T4",
        caching=True,
    )
    @dsl.component
    def echo() -> str:
        return "hello, world"

    @dsl.pipeline(name="echo-pipeline")
    def echo_pipeline():
        echo()

    pipeline_path = os.fspath(tmp_path / "pipeline.json")
    compiler.Compiler().compile(pipeline_func=echo_pipeline, package_path=pipeline_path)

    with open(pipeline_path, "r") as f:
        pipeline_json = json.load(f)

    container = pipeline_json["pipelineSpec"]["deploymentSpec"]["executors"][
        "exec-echo"
    ]["container"]
    task = pipeline_json["pipelineSpec"]["root"]["dag"]["tasks"]["echo"]

    assert container["resources"]["cpuLimit"] == 2.0
    assert container["resources"]["memoryLimit"] == 16.0
    assert container["resources"]["accelerator"]["count"] == "1"
    assert container["resources"]["accelerator"]["type"] == "NVIDIA_TESLA_T4"
    assert task["taskInfo"]["name"] == "Echo Component"
    assert task["cachingOptions"]["enableCache"] is True


def test_spec_as_function(tmp_path):
    @dsl.component
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
    compiler.Compiler().compile(pipeline_func=echo_pipeline, package_path=pipeline_path)

    with open(pipeline_path, "r") as f:
        pipeline_json = json.load(f)

    container = pipeline_json["pipelineSpec"]["deploymentSpec"]["executors"][
        "exec-echo"
    ]["container"]
    task = pipeline_json["pipelineSpec"]["root"]["dag"]["tasks"]["echo"]

    assert container["resources"]["cpuLimit"] == 2.0
    assert container["resources"]["memoryLimit"] == 16.0
    assert container["resources"]["accelerator"]["count"] == "1"
    assert container["resources"]["accelerator"]["type"] == "NVIDIA_TESLA_T4"
    assert task["taskInfo"]["name"] == "Echo Component"
    assert task["cachingOptions"]["enableCache"] is True


def test_spec_caching(tmp_path):
    @spec(caching=False)
    @dsl.component
    def echo() -> str:
        return "hello, world"

    @dsl.pipeline(name="echo-pipeline")
    def echo_pipeline():
        echo()

    pipeline_path = os.fspath(tmp_path / "pipeline.json")
    compiler.Compiler().compile(pipeline_func=echo_pipeline, package_path=pipeline_path)

    with open(pipeline_path, "r") as f:
        pipeline_json = json.load(f)

    task = pipeline_json["pipelineSpec"]["root"]["dag"]["tasks"]["echo"]

    assert "enableCache" not in task["cachingOptions"]


def test_spec_with_multiple_decorators(tmp_path):
    default_spec = spec(cpu="2", memory="16G")

    @spec(cpu="1")
    @default_spec
    @dsl.component
    def echo() -> str:
        return "hello, world"

    @dsl.pipeline(name="echo-pipeline")
    def echo_pipeline():
        echo()

    pipeline_path = os.fspath(tmp_path / "pipeline.json")
    compiler.Compiler().compile(pipeline_func=echo_pipeline, package_path=pipeline_path)

    with open(pipeline_path, "r") as f:
        pipeline_json = json.load(f)

    container = pipeline_json["pipelineSpec"]["deploymentSpec"]["executors"][
        "exec-echo"
    ]["container"]

    assert container["resources"]["cpuLimit"] == 1.0
    assert container["resources"]["memoryLimit"] == 16.0
