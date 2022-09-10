from typing import Optional

from kfp.v2 import dsl

from .decorators import spec


@spec(caching=False)
@dsl.component
def timestamp(
    format: str = "%Y%m%d%H%M%S",
    prefix: Optional[str] = None,
    postfix: Optional[str] = None,
    separator: str = "-",
    tz_offset: int = 0,
) -> str:
    import datetime

    tz = datetime.timezone(offset=datetime.timedelta(hours=tz_offset))
    time_string = datetime.datetime.now(tz).strftime(format)
    if prefix:
        time_string = separator.join([prefix, time_string])
    if postfix:
        time_string = separator.join([time_string, postfix])
    return time_string
