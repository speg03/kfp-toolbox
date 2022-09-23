from freezegun import freeze_time

from kfp_toolbox import components


class TestTimestamp:
    @freeze_time("2022-09-01 00:00:00")
    def test(self):
        time_string = components.timestamp.python_func()
        assert time_string == "20220901000000"

    @freeze_time("2022-09-01 00:00:00")
    def test_format(self):
        time_string = components.timestamp.python_func(format="%Y-%m-%d %H:%M:%S %Z")
        assert time_string == "2022-09-01 00:00:00 UTC"

    @freeze_time("2022-09-01 00:00:00")
    def test_offset(self):
        time_string = components.timestamp.python_func(
            format="%Y-%m-%d %H:%M:%S %Z", tz_offset=9
        )
        assert time_string == "2022-09-01 09:00:00 UTC+09:00"

    @freeze_time("2022-09-01 00:00:00")
    def test_prefix_and_postfix(self):
        time_string = components.timestamp.python_func(
            prefix="example", postfix="results"
        )
        assert time_string == "example-20220901000000-results"

    @freeze_time("2022-09-01 00:00:00")
    def test_separator(self):
        time_string = components.timestamp.python_func(
            prefix="example", postfix="results", separator="/"
        )
        assert time_string == "example/20220901000000/results"

    def test_specific(self):
        time_string = components.timestamp.python_func(format="2022-01-01")
        assert time_string == "2022-01-01"
