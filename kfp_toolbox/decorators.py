import functools
from typing import Optional

from kfp.v2.dsl import ContainerOp


def spec(
    cpu: Optional[str] = None,
    memory: Optional[str] = None,
    gpu: Optional[str] = None,
    accelerator: Optional[str] = None,
):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            task: ContainerOp = func(*args, **kwargs)
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

        return wrapper

    return decorator
