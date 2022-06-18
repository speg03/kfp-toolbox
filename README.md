# kfp-toolbox

*kfp-toolbox* is a Python library that provides useful tools for kfp (Kubeflow Pipelines SDK).

[![PyPI](https://img.shields.io/pypi/v/kfp-toolbox)](https://pypi.org/project/kfp-toolbox/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kfp-toolbox)](https://pypi.org/project/kfp-toolbox/)
[![Python Tests](https://github.com/speg03/kfp-toolbox/actions/workflows/python-tests.yml/badge.svg)](https://github.com/speg03/kfp-toolbox/actions/workflows/python-tests.yml)
[![codecov](https://codecov.io/gh/speg03/kfp-toolbox/branch/main/graph/badge.svg?token=wsW6rjrcBz)](https://codecov.io/gh/speg03/kfp-toolbox)


## Installation

```
pip install kfp-toolbox
```


## Usage

### `spec`

```python
from kfp_toolbox import spec
```

The `spec` decorator specifies the computing resources to be used by the component.

To apply this to a Python function-based component, it must be added outside of the `component` decorator.

```python
@spec(cpu="2", memory="16G")
@dsl.component
def component_function():
    ...
```

For other components, wrap the component as a function.

```python
component = kfp.components.load_component_from_file("path/to/component.yaml")
component = spec(cpu="2", memory="16G")(component)
```

If multiple `spec` decorators are stacked, the one placed further out will take precedence. For example, suppose you have created an alias `default_spec`. If you want to overwrite part of it, place a new `spec` decorator outside of the `default_spec` decorator to overwrite it.

```python
default_spec = spec(cpu="2", memory="16G")

@spec(cpu="1")
@default_spec
@dsl.component
def component_function():
    ...
```

See all available options here:

|option|type|description|examples|
|---|---|---|---|
|name|str|Display name|`"Component NAME"`|
|cpu|str|CPU limit|`"1"`, `"500m"`, ... ("m" means 1/1000)|
|memory|str|Memory limit|`"512K"`, `"16G"`, ...|
|gpu|str|GPU limit|`"1"`, `"2"`, ...|
|accelerator|str|Accelerator type|`"NVIDIA_TESLA_K80"`, `"TPU_V3"`, ...|
|caching|bool|Enable caching|`True` or `False`|
