from kfp.v2 import dsl


@dsl.component()
def echo(message: str) -> str:
    return message


@dsl.pipeline(name="echo-pipeline")
def echo_pipeline(message: str):
    echo(message)


@dsl.pipeline(name="hello-pipeline")
def hello_pipeline():
    echo("hellow, world.")
