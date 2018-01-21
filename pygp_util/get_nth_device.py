from .get_all_cl_devices import get_all_cl_gpus, get_all_cl_cpus

from typing import Optional

def get_nth_gpu(n  # type: Optional[int]
                ):
    if n is None:
        n=0
    return get_all_cl_gpus()[n]

def get_nth_cpu(n  # type: Optional[int]
                ):
    if n is None:
        n=0
    return get_all_cl_cpus()[n]