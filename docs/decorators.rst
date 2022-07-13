Decorators
==========

``spec``
--------

.. code-block:: python

    from kfp_toolbox import spec

The ``spec`` decorator specifies the computing resources to be used by the component.

To apply this to a Python function-based component, it must be added outside of the ``component`` decorator.

.. code-block:: python

    from kfp.v2 import dsl

    @spec(cpu="2", memory="16G")
    @dsl.component
    def component_function():
        ...

For other components, wrap the component as a function.

.. code-block:: python

    from kfp.components import load_component_from_file

    component = load_component_from_file("path/to/component.yaml")
    component = spec(cpu="2", memory="16G")(component)

If multiple ``spec`` decorators are stacked, the one placed further out will take precedence. For example, suppose you have created an alias ``default_spec``. If you want to overwrite part of it, place a new ``spec`` decorator outside of the ``default_spec`` decorator to overwrite it.

.. code-block:: python

    from kfp.v2 import dsl

    default_spec = spec(cpu="2", memory="16G")

    @spec(cpu="1")
    @default_spec
    @dsl.component
    def component_function():
        ...

See all available options here:

.. list-table:: Options for ``spec``
    :header-rows: 1

    * - option
      - type
      - description
      - examples
    * - name
      - str
      - Display name
      - ``"Component Name"``
    * - cpu
      - str
      - CPU limit
      - ``"1"``, ``"500m"``, ... ("m" means 1/1000)
    * - memory
      - str
      - Memory limit
      - ``"512K"``, ``"16G"``, ...
    * - gpu
      - str
      - GPU limit
      - ``"1"``, ``"2"``, ...
    * - accelerator
      - str
      - Accelerator type
      - ``"NVIDIA_TESLA_K80"``, ``"TPU_V3"``, ...
    * - caching
      - bool
      - Whether or not to enable caching
      - ``True`` or ``False``
