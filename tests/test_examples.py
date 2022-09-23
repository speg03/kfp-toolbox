import subprocess


class TestTimestampPipeline:
    def test_v1(self, tmp_path):
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

    def test(self, tmp_path):
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
