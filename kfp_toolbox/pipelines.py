import json
import os
from dataclasses import dataclass
from typing import Any, Callable, List, Mapping, Optional, Union

import yaml

ParameterValue = Union[int, float, str]


@dataclass
class Parameter:
    name: str
    type: Callable
    default: Optional[ParameterValue] = None


@dataclass
class Pipeline:
    name: str
    parameters: List[Parameter]


def _type_function_from_name(type_name: str) -> Callable:
    if type_name in {"Integer", "INT"}:
        type_function = int
    elif type_name in {"Float", "DOUBLE"}:
        type_function = float
    else:
        type_function = str

    return type_function


def _actual_parameter_value(key: str, value: ParameterValue) -> ParameterValue:
    if key in {"Integer", "intValue"}:
        actual_value = int(value)
    elif key in {"Float", "doubleValue"}:
        actual_value = float(value)
    else:
        actual_value = str(value)

    return actual_value


def _create_pipeline(pipeline_spec: Mapping[str, Any]) -> Pipeline:
    pipeline_name = pipeline_spec["pipelineSpec"]["pipelineInfo"]["name"]
    input_definitions = (
        pipeline_spec["pipelineSpec"]["root"]
        .get("inputDefinitions", {})
        .get("parameters", {})
    )
    runtime_config = pipeline_spec["runtimeConfig"].get("parameters", {})

    parameters = []
    for parameter_name, parameter_type in input_definitions.items():
        parameter = Parameter(
            name=parameter_name, type=_type_function_from_name(parameter_type["type"])
        )
        if runtime_config.get(parameter_name):
            key, value = list(runtime_config[parameter_name].items())[0]
            parameter.default = _actual_parameter_value(key, value)
        parameters.append(parameter)

    return Pipeline(name=pipeline_name, parameters=parameters)


def _create_v1_pipeline(pipeline_spec: Mapping[str, Any]) -> Pipeline:
    spec_json_str = pipeline_spec["metadata"]["annotations"][
        "pipelines.kubeflow.org/pipeline_spec"
    ]
    spec_json = json.loads(spec_json_str)
    pipeline_name = spec_json["name"]

    parameters = []
    for item in spec_json["inputs"]:
        if item["name"] in {"pipeline-root", "pipeline-name"}:
            continue
        parameter = Parameter(
            name=item["name"], type=_type_function_from_name(item["type"])
        )
        if item.get("default") is not None:
            parameter.default = _actual_parameter_value(item["type"], item["default"])
        parameters.append(parameter)

    return Pipeline(name=pipeline_name, parameters=parameters)


def load_pipeline_from_file(filepath: Union[str, os.PathLike]) -> Pipeline:
    filepath_str = os.fspath(filepath)
    with open(filepath_str, "r") as f:
        pipeline_spec = yaml.safe_load(f)

    if (
        "pipelineSpec" in pipeline_spec
        and "root" in pipeline_spec["pipelineSpec"]
        and "pipelineInfo" in pipeline_spec["pipelineSpec"]
        and "runtimeConfig" in pipeline_spec
    ):
        pipeline = _create_pipeline(pipeline_spec)
    elif (
        "metadata" in pipeline_spec
        and "annotations" in pipeline_spec["metadata"]
        and "pipelines.kubeflow.org/pipeline_spec"
        in pipeline_spec["metadata"]["annotations"]
    ):
        pipeline = _create_v1_pipeline(pipeline_spec)
    else:
        raise ValueError(f"invalid schema: {filepath_str}")

    return pipeline
