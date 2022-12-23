from unittest.mock import patch

from kfp_toolbox.pipeline_jobs import submit_pipeline_job


class TestSubmitPipelineJob:
    @patch("google.cloud.aiplatform.PipelineJob")
    @patch("kfp.Client")
    def test_no_endpoints(self, mock_kfp, mock_aip):
        submit_pipeline_job(
            pipeline_file="/path/to/file",
            arguments={"param": 1},
            run_name="test-run",
            experiment_name="test-experiment",
        )

        mock_kfp.assert_not_called()
        mock_aip.assert_called_once_with(
            display_name=None,
            template_path="/path/to/file",
            job_id="test-run",
            pipeline_root=None,
            parameter_values={"param": 1},
            enable_caching=None,
            encryption_spec_key_name=None,
            labels=None,
            project=None,
            location=None,
        )
        mock_aip.return_value.submit.assert_called_once_with(
            service_account=None, network=None, experiment="test-experiment"
        )

    @patch("google.cloud.aiplatform.PipelineJob")
    @patch("kfp.Client")
    def test_endpoint(self, mock_kfp, mock_aip):
        submit_pipeline_job(
            pipeline_file="/path/to/file",
            arguments={"param": 1},
            run_name="test-run",
            experiment_name="test-experiment",
            endpoint="http://localhost:8080",
        )

        mock_aip.assert_not_called()
        mock_kfp.assert_called_once_with(
            host="http://localhost:8080",
            client_id=None,
            namespace="kubeflow",
            other_client_id=None,
            other_client_secret=None,
        )
        mock_kfp.return_value.create_run_from_pipeline_package.assert_called_once_with(
            pipeline_file="/path/to/file",
            arguments={"param": 1},
            run_name="test-run",
            experiment_name="test-experiment",
            namespace=None,
            pipeline_root=None,
            enable_caching=None,
            service_account=None,
        )
