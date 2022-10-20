import warnings
from typing import Optional

from kfp.v2 import dsl

from .decorators import caching, override_docstring


@caching(False)
@override_docstring()
@dsl.component()
def timestamp(
    format: str = "%Y%m%d%H%M%S",
    prefix: Optional[str] = None,
    suffix: Optional[str] = None,
    postfix: Optional[str] = None,
    separator: str = "-",
    tz_offset: int = 0,
) -> str:
    """Generate a time string in a specified format.

    It adds a :attr:`prefix` or :attr:`suffix` to the time string generated from the
    format, along with a :attr:`separator`. :attr:`tz_offset` can be specified to
    represent a time zone other than UTC.

    This function is used as a component. Since caching is disabled by default, it is
    executed each time at the current time unless caching is enabled in the pipeline.

    Args:
        format (str, optional): Time format string. Strings that cannot be interpreted
            as a format string are output as is. Defaults to "%Y%m%d%H%M%S".
        prefix (Optional[str], optional): A prefix string to be prepended to the format
            string. Defaults to None.
        suffix (Optional[str], optional): A suffix string to be added after the
            format string. Defaults to None.
        postfix (Optional[str], optional): DEPRECATED: Use :attr:`suffix` instead.
            A postfix string to be added after the format string. Defaults to None.
        separator (str, optional): Separator to be added between the format string,
            prefix and suffix. Defaults to "-".
        tz_offset (int, optional): Time zone offset specified in hours. Defaults to 0.

    Returns:
        str: The current time string represented by a format string. A prefix and
        suffix string separated by a separator is appended.

    .. deprecated:: 0.5.0
        :attr:`postfix` argument is deprecated. Use :attr:`suffix` instead.

    """

    import datetime

    tz = datetime.timezone(offset=datetime.timedelta(hours=tz_offset))
    time_string = datetime.datetime.now(tz).strftime(format)
    if prefix:
        time_string = separator.join([prefix, time_string])
    if postfix:
        warnings.warn(
            "`postfix` argument is deprecated. Use `suffix` instead.",
            DeprecationWarning,
        )
        suffix = postfix
    if suffix:
        time_string = separator.join([time_string, suffix])
    return time_string
