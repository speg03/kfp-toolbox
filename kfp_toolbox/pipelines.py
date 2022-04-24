import json
from dataclasses import dataclass
from typing import Dict, Mapping, Optional, Union

ParameterValue = Union[int, float, str]


@dataclass
class Parameter:
    name: str
    type: str
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

    with open(package_path, "r") as f:
        pipeline = json.load(f)

    input_definitions = (
        pipeline.get("pipelineSpec", {})
        .get("root", {})
        .get("inputDefinitions", {})
        .get("parameters", {})
    )
    parameters = {
        k: Parameter(name=k, type=v["type"]) for k, v in input_definitions.items()
    }

    runtime_config = pipeline.get("runtimeConfig", {}).get("parameters", {})
    for k, v in runtime_config.items():
        parameters[k].default = _default_value(v)

    return parameters
