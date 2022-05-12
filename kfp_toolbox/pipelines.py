import json
from dataclasses import dataclass
from typing import Callable, Dict, Mapping, Optional, Union

ParameterValue = Union[int, float, str]


@dataclass
class Parameter:
    name: str
    type: Callable
    default: Optional[ParameterValue] = None


def extract_pipeline_parameters(package_path: str) -> Dict[str, Parameter]:
    def _default_value(runtime_config: Mapping[str, ParameterValue]) -> ParameterValue:
        if "intValue" in runtime_config:
            value = int(runtime_config["intValue"])
        elif "doubleValue" in runtime_config:
            value = float(runtime_config["doubleValue"])
        elif "stringValue" in runtime_config:
            value = str(runtime_config["stringValue"])
        else:
            raise ValueError(
                f"Unknown config: {runtime_config}, "
                "Expected: intValue, doubleValue or stringValue"
            )
        return value

    def _type_function_from_name(type_name: str) -> Callable:
        if type_name == "INT":
            type_function = int
        elif type_name == "DOUBLE":
            type_function = float
        elif type_name == "STRING":
            type_function = str
        else:
            raise ValueError(
                f"Unknown type: {type_name}, Expected: INT, DOUBLE or STRING"
            )
        return type_function

    with open(package_path, "r") as f:
        pipeline = json.load(f)

    if (
        "pipelineSpec" not in pipeline
        or "runtimeConfig" not in pipeline
        or "root" not in pipeline["pipelineSpec"]
    ):
        raise ValueError(
            "Expected JSON schema: "
            '{"pipelineSpec": {"root": ...}, "runtimeConfig": ...}'
        )

    input_definitions = (
        pipeline["pipelineSpec"]["root"]
        .get("inputDefinitions", {})
        .get("parameters", {})
    )

    parameters = {
        k: Parameter(name=k, type=_type_function_from_name(v["type"]))
        for k, v in input_definitions.items()
    }

    runtime_config = pipeline["runtimeConfig"].get("parameters", {})
    for k, v in runtime_config.items():
        parameters[k].default = _default_value(v)

    return parameters
