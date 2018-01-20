import os
import time
import numpy as np
import pyopencl as cl

import cv_pubsubs.cv_webcam_pub as w


os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1'

my_dir = os.path.dirname(os.path.abspath(__file__))

if False:
    from typing import Tuple


def get_all_cl_gpus():
    gpu_list = []
    for platf in cl.get_platforms():
        gpu_list.extend(platf.get_devices(cl.device_type.GPU))

    return gpu_list


def read_cl_file(shader_file):
    with open(shader_file) as rgc:
        cl_str = rgc.read()
    return cl_str


def compile_rgc(
        relative_color_filter=True,
        edge_filter=True,
        time_filter=True,
        combine_time_and_color=False,
        shader_file=None,
        request_size=(1280, 720),  # type: Tuple[int, int]
        gpu=None
):
    colors = 3
    if shader_file is None:
        shader_file = my_dir + os.sep + 'retinal shaders' + os.sep + 'RetinalGanglianFilter.cl'
    cl_str = read_cl_file(shader_file).format(request_size[0], request_size[1], colors, 127)

    if gpu is None:
        gpus = get_all_cl_gpus()  # get last gpu (typically dedicated one on devices with multiple)
        gpu = [gpus[0]]

    ctx = cl.Context(gpu)
    queue = cl.CommandQueue(ctx)
    mf = cl.mem_flags

    options = [r"-I", my_dir + os.sep + 'retinal shaders']
    if relative_color_filter:
        options.extend(["-D", "RELATIVE_COLOR_FILTER"])
        if combine_time_and_color:
            options.extend(["-D", "RELATIVE_TIME_FILTER"])
    if edge_filter:
        options.extend(["-D", "EDGE_FILTER"])
    if time_filter:
        options.extend(["-D", "TIME_FILTER"])

    prog = cl.Program(ctx, cl_str).build(options=options)

    return prog, queue, mf, ctx


allCallbacks = []


def run_rgc(
        request_size=(1280, 720),  # type: Tuple[int, int]
        relative_color_filter=True,
        edge_filter=True,
        time_filter=True,
        combine_time_and_color=True
):
    global allCallbacks

    prog, queue, mf, ctx = compile_rgc(
        relative_color_filter=relative_color_filter,
        edge_filter=edge_filter,
        time_filter=time_filter,
        combine_time_and_color=combine_time_and_color,
        request_size=request_size)

    if relative_color_filter:
        color_np = np.full((request_size[1], request_size[0], 3), 127, dtype=np.uint8)
        color_buf = cl.Buffer(ctx, mf.WRITE_ONLY, color_np.nbytes)

    if edge_filter:
        edge_np = np.full((request_size[1], request_size[0], 1), 127, dtype=np.uint8)
        edge_buf = cl.Buffer(ctx, mf.WRITE_ONLY, edge_np.nbytes)

    if time_filter:
        avg_np = np.full((request_size[1], request_size[0], 3), 127, dtype=np.uint8)
        avg_buf = cl.Buffer(ctx, mf.WRITE_ONLY, avg_np.nbytes)

    def gpu_main_update(frame  # type: np.ndarray
                        ):
        in_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=frame)

        time32 = (time.time() * 1000) % (2 ** 32)
        args = [queue, (request_size[1], request_size[0], 3), (8, 8, 1), in_buf, np.uint32(time32)]

        buffs = []
        if relative_color_filter:
            buffs.append(color_buf)
        if edge_filter:
            buffs.append(edge_buf)
        if time_filter:
            buffs.append(avg_buf)
        args.extend(buffs)

        prog.rgc(*args)

        arrays = []
        if relative_color_filter:
            arrays.append(color_np)
        if edge_filter:
            arrays.append(edge_np)
        if time_filter:
            arrays.append(avg_np)

        for b in range(len(buffs)):
            cl.enqueue_copy(queue, arrays[b], buffs[b]).wait()

        return arrays

    allCallbacks.append(gpu_main_update)

import cv_pubsubs as cvp
def display_rgc(cam,
                request_size=(1280, 720),  # type: Tuple[int, int]
                ):
    run_rgc(request_size)

    def cam_handler(frame, cam_id):
        cvp.frameDict[str(cam_id) + "Frame"] = frame

    cam_thread = cvp.frame_handler_thread(cam, cam_handler)

    cvp.sub_win_loop(names=['RGC Relative Color Filter',
                            'RGC Edge Filter',
                            'RGC Time Averaging Filter'],
                 input_vid_global_names=[str(cam) + 'Frame'],
                 callbacks=allCallbacks)

    return cam_thread


if __name__ == '__main__':
    t = display_rgc(0, (1280, 720))
    t.join()
