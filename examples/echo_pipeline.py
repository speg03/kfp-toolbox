from kfp.v2 import dsl

from kfp_toolbox import spec


@spec(name="echo-hello", cpu="1", memory="4G")
@dsl.component()
def echo(message: str) -> str:
    return message


@dsl.pipeline(name="echo-pipeline")
def echo_pipeline(message: str = "hello, world"):
    echo(message)
