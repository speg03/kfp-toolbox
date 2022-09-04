from kfp.v2 import dsl

from kfp_toolbox.components import timestamp


@dsl.pipeline(name="timestamp-pipeline")
def timestamp_pipeline():
    timestamp()
