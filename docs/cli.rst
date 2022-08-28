Command Line Interface
======================

``kfp-toolbox`` command can be used.

Global options
--------------

Help:

.. code-block:: none

    kfp-toolbox --help

Show the installed version:

.. code-block:: none

    kfp-toolbox --version

``kfp-toolbox submit``
----------------------

``submit`` subcommand submits pipeline jobs to the appropriate environment.

Vertex AI Pipelines
^^^^^^^^^^^^^^^^^^^

To submit a job to Vertex AI Pipelines, a pipeline package must be created using the V2 compiler.

.. code-block:: none
    
    dsl-compile-v2 --py /path/to/pipeline.py --function pipeline \
        --output ./pipeline.json

If an ``--endpoint`` option is not specified, the job is submitted to Vertex AI Pipelines.

.. code-block:: none

    kfp-toolbox submit -f ./pipeline.json

Kubeflow Pipelines
^^^^^^^^^^^^^^^^^^

To submit a job to Kubeflow Pipelines, a pipeline package must be created using the V1 compiler with ``V2_COMPATIBLE`` mode.

.. code-block:: none

    dsl-compile --py /path/to/pipeline.py --function pipeline \
        --output ./pipeline.yaml \
        --mode V2_COMPATIBLE

If an ``--endpoint`` option is specified, the job is submitted to Kubeflow Pipelines pointed to by that endpoint.

.. code-block:: none

    kfp-toolbox submit -f ./pipeline.yaml --endpoint http://localhost:8080

Pipeline parameters
^^^^^^^^^^^^^^^^^^^

Pipeline parameters can be specified after a double dash (``--``).

.. code-block:: none

    kfp-toolbox submit -f ./pipeline.json -- \
        --parameter-name value \
        --another-parameter-name another_value

Pipeline parameters defined in the pipeline package can be viewed by specifying ``--help`` option.

.. code-block:: none

    kfp-toolbox submit -f ./pipeline.json --help
