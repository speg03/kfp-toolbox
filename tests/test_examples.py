import subprocess


def test_echo_pipeline_v1(tmp_path):
    package_path = tmp_path / "echo_pipeline.yaml"
    process = subprocess.run(
        [
            "dsl-compile",
            "--mode=V2_COMPATIBLE",
            "--py=./examples/echo_pipeline.py",
            "--function=echo_pipeline",
            f"--output={package_path}",
        ]
    )
    assert process.returncode == 0
    assert package_path.exists()


def test_echo_pipeline(tmp_path):
    package_path = tmp_path / "echo_pipeline.json"
    process = subprocess.run(
        [
            "dsl-compile-v2",
            "--py=./examples/echo_pipeline.py",
            "--function=echo_pipeline",
            f"--output={package_path}",
        ]
    )
    assert process.returncode == 0
    assert package_path.exists()


def test_timestamp_pipeline_v1(tmp_path):
    package_path = tmp_path / "timestamp_pipeline.yaml"
    process = subprocess.run(
        [
            "dsl-compile",
            "--mode=V2_COMPATIBLE",
            "--py=./examples/timestamp_pipeline.py",
            "--function=timestamp_pipeline",
            f"--output={package_path}",
        ]
    )
    assert process.returncode == 0
    assert package_path.exists()


def test_timestamp_pipeline(tmp_path):
    package_path = tmp_path / "timestamp_pipeline.json"
    process = subprocess.run(
        [
            "dsl-compile-v2",
            "--py=./examples/timestamp_pipeline.py",
            "--function=timestamp_pipeline",
            f"--output={package_path}",
        ]
    )
    assert process.returncode == 0
    assert package_path.exists()
