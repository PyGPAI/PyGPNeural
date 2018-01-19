import os

import numpy as np
import pyopencl as cl

from cv_pubsubs import cv_webcam_pub
import time

if False:
    from typing import Tuple
"""def read_in_file(*shader_file):
    '''shader_file = open(script_dir+os.sep+os.sep.join(shader_file))
    shader_text = shader_file.read()
    shader_file.close()'''

    return shader_text"""

my_dir = os.path.dirname(os.path.abspath(__file__))


def get_all_cl_gpus():
    gpu_list = []
    for platf in cl.get_platforms():
        gpu_list.extend(platf.get_devices(cl.device_type.GPU))

    return gpu_list


def read_cl_file(shader_file):
    with open(shader_file) as rgc:
        cl_str = rgc.read()
    return cl_str


def compile_rng(
        shader_file=None,
        request_size=(1280, 720),  # type: Tuple[int, int]
        gpu=None
):
    colors = 3
    if shader_file is None:
        shader_file = my_dir + os.sep + 'retinal shaders' + os.sep + 'rng.cl'
    cl_str = read_cl_file(shader_file).format(request_size[0], request_size[1], colors)

    if gpu is None:
        gpus = get_all_cl_gpus()  # get last gpu (typically dedicated one on devices with multiple)
        gpu = [gpus[0]]

    ctx = cl.Context(gpu)
    queue = cl.CommandQueue(ctx)
    mf = cl.mem_flags
    prog = cl.Program(ctx, cl_str).build()

    return prog, queue, mf, ctx


allCallbacks = []


def run_rng(
        request_size=(1280, 720),  # type: Tuple[int, int]
):
    global allCallbacks

    prog, queue, mf, ctx = compile_rng(
        request_size=request_size)

    out_np = np.zeros((request_size[1], request_size[0], 3), dtype=np.uint8)
    out_buf = cl.Buffer(ctx, mf.WRITE_ONLY, out_np.nbytes)

    def gpu_main_update(frame  # type: np.ndarray
                        ):
        in_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=frame)

        time32 = (time.time() * 1000) % (2 ** 32)
        prog.xxhash_test(queue, (request_size[1], request_size[0]), None, in_buf, np.uint32(time32), out_buf)

        cl.enqueue_copy(queue, out_np, out_buf).wait()

        return out_np

    allCallbacks.append(gpu_main_update)


def display_rng(cam,
                request_size=(1280, 720),  # type: Tuple[int, int]
                ):
    from cv_pubsubs.cv_window_sub import frameDict, cv_win_sub

    run_rng(request_size)

    def cam_handler(frame, cam_id):
        frameDict[str(cam_id) + "Frame"] = frame

    cam_thread = cv_webcam_pub.init_cv_cam_pub_handler(cam, cam_handler)

    cv_win_sub(names=[str(cam)],
               inputVidGlobalNames=[str(cam) + 'Frame'],
               callbacks=allCallbacks)

    return cam_thread


if __name__ == '__main__':
    t = display_rng(1, (1280, 720))
    t.join()
