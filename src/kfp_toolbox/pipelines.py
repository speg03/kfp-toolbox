import json
import os
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Optional, Sequence, Union

import yaml

ParameterValue = Union[int, float, str]


@dataclass
class Parameter:
    """Pipeline parameter.

    A class that represents a single pipeline parameter.

    Attributes:
        name: A name of the parameter.
        type: A type function of the parameter.
        default: A default value of the parameter.

    """

    name: str
    type: Callable
    default: Optional[ParameterValue] = None


@dataclass
class Pipeline:
    """Pipeline.

    A class that summarizes pipeline information.

    Attributes:
        name: A name of the pipeline.
        parameters: A sequence of the pipeline parameters.

    """

    name: str
    parameters: Sequence[Parameter]


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
    """Load a pipeline object from the pipeline file.

    Load a :class:`Pipeline` object from a pre-compiled file that represents
    the pipeline.

    Args:
        filepath (Union[str, os.PathLike]): The path of the pre-compiled file that
            represents the pipeline.

    Raises:
        ValueError: If the :attr:`filepath` file has an invalid schema.

    Returns:
        Pipeline: An object that represents the pipeline.

    """

    filepath_str = os.fspath(filepath)
    with open(filepath_str, "r") as f:
        pipeline_spec = yaml.safe_load(f)

    if (
        isinstance(pipeline_spec, dict)
        and "pipelineSpec" in pipeline_spec
        and "root" in pipeline_spec["pipelineSpec"]
        and "pipelineInfo" in pipeline_spec["pipelineSpec"]
        and "runtimeConfig" in pipeline_spec
    ):
        pipeline = _create_pipeline(pipeline_spec)
    elif (
        isinstance(pipeline_spec, dict)
        and "metadata" in pipeline_spec
        and "annotations" in pipeline_spec["metadata"]
        and "pipelines.kubeflow.org/pipeline_spec"
        in pipeline_spec["metadata"]["annotations"]
    ):
        pipeline = _create_v1_pipeline(pipeline_spec)
    else:
        raise ValueError(f"invalid schema: {filepath_str}")

    return pipeline


def submit_pipeline_job(
    pipeline_file: Union[str, os.PathLike],
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
    project: Optional[str] = None,
    location: Optional[str] = None,
    network: Optional[str] = None,
):
    """Submit a pipeline job.

    Submit a pipeline job to the appropriate environment. If an :attr:`endpoint` is
    specified, it is considered an instance of Kubeflow Pipelines. Otherwise, attempt
    to submit to Vertex AI Pipelines.

    Args:
        pipeline_file (Union[str, os.PathLike]): Path of the pipeline package file.
        endpoint (Optional[str], optional): Endpoint of the KFP API service to connect.
            Used only for Kubeflow Pipelines. Defaults to None.
        iap_client_id (Optional[str], optional): The client ID used by Identity-Aware
            Proxy. Used only for Kubeflow Pipelines. Defaults to None.
        api_namespace (str, optional): Kubernetes namespace to connect to the KFP API.
            Used only for Kubeflow Pipelines. Defaults to "kubeflow".
        other_client_id (Optional[str], optional): The client ID used to obtain
            the auth codes and refresh tokens. Used only for Kubeflow Pipelines.
            Defaults to None.
        other_client_secret (Optional[str], optional): The client secret used to obtain
            the auth codes and refresh tokens. Used only for Kubeflow Pipelines.
            Defaults to None.
        arguments (Optional[Mapping[str, Any]], optional): Arguments to the pipeline
            function provided as a dict. Defaults to None.
        run_name (Optional[str], optional): Name of the run to be shown in the UI.
            Defaults to None.
        experiment_name (Optional[str], optional): Name of the experiment to add the
            run to. Defaults to None.
        namespace (Optional[str], optional): Kubernetes namespace where the pipeline
            runs are created. Used only for Kubeflow Pipelines. Defaults to None.
        pipeline_root (Optional[str], optional): The root path of the pipeline outputs.
            Defaults to None.
        enable_caching (Optional[bool], optional): Whether or not to enable caching for
            the run. Defaults to None.
        service_account (Optional[str], optional): Specifies which Kubernetes service
            account this run uses. Defaults to None.
        encryption_spec_key_name (Optional[str], optional): The Cloud KMS resource
            identifier of the customer managed encryption key used to protect the job.
            Used only for Vertex AI Pipelines. Defaults to None.
        labels (Optional[Mapping[str, str]], optional): The user defined metadata to
            organize PipelineJob. Used only for Vertex AI Pipelines. Defaults to None.
        project (Optional[str], optional): The project that you want to run this
            PipelineJob in. Used only for Vertex AI Pipelines. Defaults to None.
        location (Optional[str], optional): Location to create PipelineJob. Used only
            for Vertex AI Pipelines. Defaults to None.
        network (Optional[str], optional): The full name of the Compute Engine network
            to which the job should be peered. Used only for Vertex AI Pipelines.
            Defaults to None.

    """

    pipeline_file_str = os.fspath(pipeline_file)

    if endpoint:  # Kubeflow Pipelines
        import kfp

        client = kfp.Client(
            host=endpoint,
            client_id=iap_client_id,
            namespace=api_namespace,
            other_client_id=other_client_id,
            other_client_secret=other_client_secret,
        )
        client.create_run_from_pipeline_package(
            pipeline_file=pipeline_file_str,
            arguments=arguments,  # type: ignore
            run_name=run_name,
            experiment_name=experiment_name,
            namespace=namespace,
            pipeline_root=pipeline_root,
            enable_caching=enable_caching,
            service_account=service_account,
        )
    else:  # Vertex AI Pipelines
        from google.cloud import aiplatform

        new_labels = dict(labels) if labels else {}
        if experiment_name:
            new_labels = {"experiment": experiment_name}

        job = aiplatform.PipelineJob(
            display_name=None,  # type: ignore  # will be generated
            template_path=pipeline_file_str,
            job_id=run_name,
            pipeline_root=pipeline_root,
            parameter_values=arguments,  # type: ignore
            enable_caching=enable_caching,
            encryption_spec_key_name=encryption_spec_key_name,
            labels=new_labels,
            project=project,
            location=location,
        )
        job.submit(service_account=service_account, network=network)
