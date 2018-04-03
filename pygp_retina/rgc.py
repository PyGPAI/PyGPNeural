import os
import numpy as np
import pyopencl as cl
import time

import math as m
import cv2

import pygp_util as pgpu
from .shader_util import shader_dir as rgc_shader_dir

if False:
    from typing import Tuple


def rgc_program(
                relative_color_filter=True,
                edge_filter=True,
                time_filter=True,
                combine_time_and_color=False,
                request_size=(1280, 720),  # type: Tuple[int, int]
                gpu=None
                ):  # type: (...)->pgpu.ShaderProgram
    cl_str = pgpu.format_read_file(shader_file=rgc_shader_dir + os.sep + 'RetinalGanglianFilter.cl',
                                   format_args=(request_size[0], request_size[1], 3, 127)
                                   )

    shady_p = pgpu.ShaderProgram(gpu)

    options = [r"-I", pgpu.shader_dir]
    if relative_color_filter:
        options.extend(["-D", "RELATIVE_COLOR_FILTER"])
        if combine_time_and_color:
            options.extend(["-D", "RELATIVE_TIME_FILTER"])
    if edge_filter:
        options.extend(["-D", "EDGE_FILTER"])
    if time_filter:
        options.extend(["-D", "TIME_FILTER"])

    shady_p.build_program(cl_str, options)

    return shady_p

def rgc_nocl_callback(
        request_size=(1280, 720),  # type: Tuple[int, int]
        relative_color_filter=True,
        edge_filter=True,
        time_filter=False,
        combine_time_and_color=False,
        gpu=None
):
    #todo: add color center surround filters here and call in function

    def gpu_main_update(frame  # type: np.ndarray
                        ):
        diag = m.sqrt(2)
        center_surround = np.array([[-diag,-1, -diag], [-1, 4+diag*4, -1], [-diag, -1, -diag]])
        surround_center = np.array([[diag, 1, diag], [1, -4 - diag * 4, 1], [diag, 1, diag]])
        center_surround_frame = cv2.filter2D(frame, -1, center_surround)
        surround_center_frame = cv2.filter2D(frame, -1, surround_center)
        edge_frame = (np.full_like(frame,127, dtype=np.uint8)+(center_surround_frame/2) - (surround_center_frame/2)).astype(np.uint8)
        return [edge_frame, center_surround_frame, surround_center_frame ]

    return gpu_main_update

def rgc_callback(
        request_size=(1280, 720),  # type: Tuple[int, int]
        relative_color_filter=True,
        edge_filter=True,
        time_filter=False,
        combine_time_and_color=False,
        gpu=None
):
    p = rgc_program(
        relative_color_filter=relative_color_filter,
        edge_filter=edge_filter,
        time_filter=time_filter,
        combine_time_and_color=combine_time_and_color,
        request_size=request_size,
        gpu=gpu
    )

    if relative_color_filter:
        color_np = np.full((request_size[1], request_size[0], 3), 127, dtype=np.uint8)
        color_buf = cl.Buffer(p.ctx, p.mf.WRITE_ONLY, color_np.nbytes)

    if edge_filter:
        edge_np = np.full((request_size[1], request_size[0], 1), 127, dtype=np.uint8)
        edge_buf = cl.Buffer(p.ctx, p.mf.WRITE_ONLY, edge_np.nbytes)

    if time_filter:
        avg_np = np.full((request_size[1], request_size[0], 3), 127, dtype=np.uint8)
        avg_buf = cl.Buffer(p.ctx, p.mf.WRITE_ONLY, avg_np.nbytes)

    def gpu_main_update(frame  # type: np.ndarray
                        ):
        in_buf = cl.Buffer(p.ctx, p.mf.READ_ONLY | p.mf.COPY_HOST_PTR, hostbuf=frame)

        time32 = (time.time() * 1000) % (2 ** 32)
        args = [p.queue, (request_size[1], request_size[0], 3), (8, 8, 1), in_buf, np.uint32(time32)]

        buffs = []
        if relative_color_filter:
            buffs.append(color_buf)
        if edge_filter:
            buffs.append(edge_buf)
        if time_filter:
            buffs.append(avg_buf)
        args.extend(buffs)

        p.build.rgc(*args)

        arrays = []
        if relative_color_filter:
            arrays.append(color_np)
        if edge_filter:
            arrays.append(edge_np)
        if time_filter:
            arrays.append(avg_np)

        for b in range(len(buffs)):
            cl.enqueue_copy(p.queue, arrays[b], buffs[b]).wait()

        return arrays

    return gpu_main_update
