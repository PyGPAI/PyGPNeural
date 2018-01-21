import pyopencl as cl


def get_all_cl_gpus():
    gpu_list = []
    for platf in cl.get_platforms():
        gpu_list.extend(platf.get_devices(cl.device_type.GPU))

    return gpu_list


def get_all_cl_cpus():
    cpu_list = []
    for platf in cl.get_platforms():
        cpu_list.extend(platf.get_devices(cl.device_type.CPU))

    return cpu_list
