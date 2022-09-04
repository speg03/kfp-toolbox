from freezegun import freeze_time

from kfp_toolbox import components


@freeze_time("2022-09-01 00:00:00")
def test_timestamp():
    time_string = components.timestamp.python_func()  # type: ignore
    assert time_string == "20220901000000"


@freeze_time("2022-09-01 00:00:00")
def test_timestamp_format():
    time_string = components.timestamp.python_func("%Y%m%d")  # type: ignore
    assert time_string == "20220901"


@freeze_time("2022-09-01 00:00:00")
def test_timestamp_with_prefix_and_postfix():
    time_string = components.timestamp.python_func(  # type: ignore
        prefix="example", postfix="results"
    )
    assert time_string == "example-20220901000000-results"


@freeze_time("2022-09-01 00:00:00")
def test_timestamp_with_separator():
    time_string = components.timestamp.python_func(  # type: ignore
        prefix="example", postfix="results", separator="/"
    )
    assert time_string == "example/20220901000000/results"


def test_timestamp_specific():
    time_string = components.timestamp.python_func("2022-01-01")  # type: ignore
    assert time_string == "2022-01-01"
