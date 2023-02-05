import sys

import pytest


@pytest.fixture(scope="session", autouse=True)
def append_testing_modules_path():
    sys.path.append("./src")
