import functools
import warnings
from typing import Optional

from kfp.v2 import dsl


def override_docstring(docs: Optional[str] = None):
    """Override the docstring of the component.

    Args:
        docs (Optional[str], optional): The docstring to be overwritten. If None, the
            docstring of the original function is adopted. Defaults to None.

    Returns:
        Callable: A decorator function with the specified docstring.

    """

    def _decorator(func):
        if docs is not None:
            func.__doc__ = docs
        elif hasattr(func, "python_func") and func.python_func.__doc__:
            func.__doc__ = func.python_func.__doc__
        return func

    return _decorator


def spec(
    name: Optional[str] = None,
    cpu: Optional[str] = None,
    memory: Optional[str] = None,
    gpu: Optional[str] = None,
    accelerator: Optional[str] = None,
    caching: Optional[bool] = None,
):
    """Specify computing resources to be used by the component.

    This function is used as decorator. The computing resources that can be specified
    are CPU, memory, GPU, and accelerator type. In addition, the display name of the
    component and the use of cache can be specified.

    Args:
        name (Optional[str], optional): Display name for the component. Defaults to
            None.
        cpu (Optional[str], optional): CPU limit (maximum) for the component. Defaults
            to None.
        memory (Optional[str], optional): Memory limit (maximum) for the component.
            Defaults to None.
        gpu (Optional[str], optional): GPU limit (maximum) for the component. Defaults
            to None.
        accelerator (Optional[str], optional): Accelerator type requirement for the
            component. Defaults to None.
        caching (Optional[bool], optional): Caching options for this task. Defaults to
            None.

    Returns:
        Callable: A decorator function with specified computing resources.

    .. deprecated:: 0.5.0
       Use :func:`container_spec`, :func:`display_name` and :func:`caching` decorators
       instead.

    """

    warnings.warn(
        "`spec` decorator is deprecated. Use `container_spec`, `display_name` and "
        "`caching` instead.",
        DeprecationWarning,
    )

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            task: dsl.ContainerOp = func(*args, **kwargs)
            if name:
                task.set_display_name(name)
            if cpu:
                task.container.set_cpu_limit(cpu)
            if memory:
                task.container.set_memory_limit(memory)
            if gpu:
                task.container.set_gpu_limit(gpu)
            if accelerator:
                task.add_node_selector_constraint(
                    "cloud.google.com/gke-accelerator", accelerator
                )
            if caching is not None:
                task.set_caching_options(caching)
            return task

        return wrapper

    return decorator


def container_spec(
    cpu: Optional[str] = None,
    memory: Optional[str] = None,
    gpu: Optional[str] = None,
    accelerator: Optional[str] = None,
):
    """Specify computing resources to be used by the component.

    The computing resources that can be specified are CPU, memory, GPU, and accelerator
    type.

    Args:
        cpu (Optional[str], optional): CPU limit (maximum) for the component. Defaults
            to None.
        memory (Optional[str], optional): Memory limit (maximum) for the component.
            Defaults to None.
        gpu (Optional[str], optional): GPU limit (maximum) for the component. Defaults
            to None.
        accelerator (Optional[str], optional): Accelerator type requirement for the
            component. Defaults to None.

    Returns:
        Callable: A decorator function with specified computing resources.

    """

    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            task: dsl.ContainerOp = func(*args, **kwargs)
            if cpu:
                task.container.set_cpu_limit(cpu)
            if memory:
                task.container.set_memory_limit(memory)
            if gpu:
                task.container.set_gpu_limit(gpu)
            if accelerator:
                task.add_node_selector_constraint(
                    "cloud.google.com/gke-accelerator", accelerator
                )
            return task

        return _wrapper

    return _decorator


def display_name(name: str):
    """Specify a display name of the component.

    Args:
        name (str): Display name.

    Returns:
        Callable: A decorator function with specified a display name.

    """

    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            task: dsl.ContainerOp = func(*args, **kwargs)
            task.set_display_name(name)
            return task

        return _wrapper

    return _decorator


def caching(enable_caching: bool):
    """Specify a caching option of the component.

    Args:
        enable_caching (bool): Whether the component uses the cache from a previous run.

    Returns:
        Callable: A decorator function with specified a caching option.

    """

    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            task: dsl.ContainerOp = func(*args, **kwargs)
            task.set_caching_options(enable_caching)
            return task

        return _wrapper

    return _decorator
