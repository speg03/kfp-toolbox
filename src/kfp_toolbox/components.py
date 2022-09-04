from kfp.v2 import dsl

from .decorators import spec


@spec(caching=False)
@dsl.component
def timestamp(
    format: str = "%Y%m%d%H%M%S",
    prefix: str = "",
    postfix: str = "",
    separator: str = "-",
) -> str:
    from datetime import datetime

    time_string = datetime.now().strftime(format)
    if prefix:
        time_string = separator.join([prefix, time_string])
    if postfix:
        time_string = separator.join([time_string, postfix])
    return time_string
