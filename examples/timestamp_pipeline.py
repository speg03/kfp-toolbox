# type: ignore
from kfp.v2 import dsl

from kfp_toolbox import spec
from kfp_toolbox.components import timestamp


@spec(name="echo-message", cpu="1", memory="4G")
@dsl.component()
def echo(message: str) -> str:
    return message


@dsl.pipeline(name="timestamp-pipeline")
def timestamp_pipeline():
    timestamp_task = timestamp(
        format="%Y%m%d", prefix="examples", postfix="results", separator="/"
    )
    echo(timestamp_task.output)
