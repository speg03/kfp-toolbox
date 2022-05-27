import json
import os
from dataclasses import dataclass
from typing import Any, Callable, List, Mapping, Optional, Union

import kfp
import yaml
from google.auth import credentials as auth_credentials
from google.cloud import aiplatform

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


def submit_pipeline_job(
    pipeline_file: str,
    endpoint: Optional[str] = None,
    iap_client_id: Optional[str] = None,
    api_namespace: str = "kubeflow",
    other_client_id: Optional[str] = None,
    other_client_secret: Optional[str] = None,
    arguments: Optional[Mapping[str, Any]] = None,
    run_name: Optional[str] = None,
    experiment_name: Optional[str] = None,
    namespace: Optional[str] = None,
    pipeline_root: Optional[str] = None,
    enable_caching: Optional[bool] = None,
    service_account: Optional[str] = None,
    encryption_spec_key_name: Optional[str] = None,
    labels: Optional[Mapping[str, str]] = None,
    credentials: Optional[auth_credentials.Credentials] = None,
    project: Optional[str] = None,
    location: Optional[str] = None,
    network: Optional[str] = None,
):
    if endpoint:  # Kubeflow Pipelines
        client = kfp.Client(
            host=endpoint,
            client_id=iap_client_id,
            namespace=api_namespace,
            other_client_id=other_client_id,
            other_client_secret=other_client_secret,
        )
        client.create_run_from_pipeline_package(
            pipeline_file=pipeline_file,
            arguments=arguments,  # type: ignore
            run_name=run_name,
            experiment_name=experiment_name,
            namespace=namespace,
            pipeline_root=pipeline_root,
            enable_caching=enable_caching,
            service_account=service_account,
        )
    else:  # Vertex AI Pipelines
        job = aiplatform.PipelineJob(
            display_name=None,  # type: ignore  # will be generated
            template_path=pipeline_file,
            job_id=run_name,
            pipeline_root=pipeline_root,
            parameter_values=arguments,  # type: ignore
            enable_caching=enable_caching,
            encryption_spec_key_name=encryption_spec_key_name,
            labels=labels,  # type: ignore
            credentials=credentials,
            project=project,
            location=location,
        )
        job.submit(service_account=service_account, network=network)
