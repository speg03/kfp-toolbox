import os
import warnings
from typing import Any, Mapping, Optional, Union

from kfp.v2 import dsl

from . import pipeline_jobs, pipeline_parser
from .components import timestamp
from .pipeline_parser import Parameter, ParameterValue, Pipeline  # noqa: F401


@dsl.pipeline(name="timestamp-pipeline")
def timestamp_pipeline(
    format: str = "%Y%m%d%H%M%S",
    prefix: str = "",
    suffix: str = "",
    separator: str = "-",
    tz_offset: int = 0,
):
    time_string = timestamp(
        format=format,
        prefix=prefix,
        suffix=suffix,
        separator=separator,
        tz_offset=tz_offset,
    )
    return time_string


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

    .. deprecated:: 0.6.0
        Use :func:`.pipeline_parser.parse_pipeline_package` instead.

    """

    warnings.warn(
        "`load_pipeline_from_file is deprecated."
        " Use `pipeline_parser.parse_pipeline_package` instead.",
        DeprecationWarning,
    )

    return pipeline_parser.parse_pipeline_package(filepath=filepath)


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

    .. deprecated:: 0.6.0
        Use :func:`.pipeline_jobs.submit_pipeline_job` instead.

    """

    warnings.warn(
        "`pipelines.submit_pipeline_job` is deprecated."
        " Use `pipeline_jobs.submit_pipeline_job` instead.",
        DeprecationWarning,
    )

    return pipeline_jobs.submit_pipeline_job(
        pipeline_file=pipeline_file,
        endpoint=endpoint,
        iap_client_id=iap_client_id,
        api_namespace=api_namespace,
        other_client_id=other_client_id,
        other_client_secret=other_client_secret,
        arguments=arguments,
        run_name=run_name,
        experiment_name=experiment_name,
        namespace=namespace,
        pipeline_root=pipeline_root,
        enable_caching=enable_caching,
        service_account=service_account,
        encryption_spec_key_name=encryption_spec_key_name,
        labels=labels,
        project=project,
        location=location,
        network=network,
    )
