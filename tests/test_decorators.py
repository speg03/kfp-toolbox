import json
import os

from kfp.v2 import compiler, dsl

from kfp_toolbox import spec


def test_spec(tmp_path):
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
    echo_task = pipeline_json["pipelineSpec"]["root"]["dag"]["tasks"]["echo"]

    assert container["resources"]["cpuLimit"] == 2.0
    assert container["resources"]["memoryLimit"] == 16.0
    assert container["resources"]["accelerator"]["count"] == "1"
    assert container["resources"]["accelerator"]["type"] == "NVIDIA_TESLA_T4"
    assert echo_task["taskInfo"]["name"] == "Echo Component"
    assert echo_task["cachingOptions"]["enableCache"] is True