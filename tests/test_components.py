from freezegun import freeze_time

from kfp_toolbox import components


@freeze_time("2022-09-01 00:00:00")
def test_timestamp():
    time_string = components.timestamp.python_func()
    assert time_string == "20220901000000"


@freeze_time("2022-09-01 00:00:00")
def test_timestamp_format():
    time_string = components.timestamp.python_func(format="%Y-%m-%d %H:%M:%S %Z")
    assert time_string == "2022-09-01 00:00:00 UTC"


@freeze_time("2022-09-01 00:00:00")
def test_timestamp_with_offset():
    time_string = components.timestamp.python_func(
        format="%Y-%m-%d %H:%M:%S %Z", tz_offset=9
    )
    assert time_string == "2022-09-01 09:00:00 UTC+09:00"


@freeze_time("2022-09-01 00:00:00")
def test_timestamp_with_prefix_and_postfix():
    time_string = components.timestamp.python_func(prefix="example", postfix="results")
    assert time_string == "example-20220901000000-results"


@freeze_time("2022-09-01 00:00:00")
def test_timestamp_with_separator():
    time_string = components.timestamp.python_func(
        prefix="example", postfix="results", separator="/"
    )
    assert time_string == "example/20220901000000/results"


def test_timestamp_specific():
    time_string = components.timestamp.python_func(format="2022-01-01")
    assert time_string == "2022-01-01"
