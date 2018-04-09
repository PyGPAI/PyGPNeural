import cv2
import os
import pyopencl as cl
import pygp_util as pgpu
from .shader_util import shader_dir as v1_shader_dir
import time

import math as m

import numpy as np
if False:
    from typing import Tuple

from pygp_retina import rgc_callback, rgc_nocl_callback

def v1_program(
               request_size=(1280,720),
               gpu=None
               ):
    cl_str = pgpu.format_read_file(shader_file=v1_shader_dir + os.sep + 'v1_shader.cl',
                                   format_args=(request_size[0], request_size[1], "(int3)(127,127,127)"))

    shady_p = pgpu.ShaderProgram(gpu)

    options = [r"-I", v1_shader_dir , r"-I", pgpu.shader_dir]

    shady_p.build_program(cl_str, options)

    return shady_p


def v1_nocl_callback(
        request_size=(1280, 720),  # type: Tuple[int, int]
        gpu=0
):
    rgc_cb = rgc_nocl_callback(request_size=request_size,
                          relative_color_filter=True,
                          edge_filter=False,
                          time_filter=False,
                          combine_time_and_color=False,
                          gpu=1)

    def gpu_main_update(frame  # type: np.ndarray
                        ):
        edge = cv2.cvtColor(rgc_cb(frame)[0], cv2.COLOR_RGB2GRAY)
        diag = m.sqrt(2)

        north = np.array([[diag,   1,  diag],
                          [0,      0,     0],
                          [-diag, -1, -diag]])
        north_east = np.array([[ 0,     1, diag],
                               [-1,     0, 1],
                               [-diag, -1, 0]])
        east = np.array([[-diag, 0, diag],
                         [-1,    0, 1],
                         [-diag, 0, diag]])
        south_east = np.array([[-diag, -1, 0],
                               [-1,     0, 1],
                               [ 0, 1, diag]])
        north_frame = cv2.filter2D(edge, -1, north)
        north_east_frame = cv2.filter2D(edge, -1, north_east)
        east_frame = cv2.filter2D(edge, -1, east)
        south_east_frame = cv2.filter2D(edge, -1, south_east)

        hue_num = (north_frame*0+north_east_frame*85+east_frame*170+south_east_frame*255).astype(np.int)
        hue_div = (north_frame+north_east_frame+east_frame+south_east_frame).astype(np.int)

        with np.errstate(divide='ignore', invalid='ignore'):
            hue = hue_num/hue_div
            hue[hue==np.inf]=0
            hue = np.nan_to_num(hue)

        hsv = np.full((hue.shape + (3,)), 255, np.uint8)
        hsv[:,:,0] = hue[:,:]

        hsv_col = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        return [ hsv_col, north_frame, north_east_frame, east_frame, south_east_frame
                ]

    return gpu_main_update

def v1_callback(
        request_size=(1280, 720),  # type: Tuple[int, int]
        gpu=0
):
    rgc_cb = rgc_callback(request_size=request_size,
                          relative_color_filter=True,
                          edge_filter=False,
                          time_filter=False,
                          combine_time_and_color=False,
                          gpu=1)

    p = v1_program(request_size=request_size,
                   gpu=gpu)

    by_np = np.full((request_size[1], request_size[0],1), 127, dtype= np.uint8)
    by_buf= cl.Buffer(p.ctx, p.mf.WRITE_ONLY, by_np.nbytes)

    yb_np = np.full((request_size[1], request_size[0], 1), 127, dtype=np.uint8)
    yb_buf = cl.Buffer(p.ctx, p.mf.WRITE_ONLY, yb_np.nbytes)

    bw_np = np.full((request_size[1], request_size[0], 1), 127, dtype=np.uint8)
    bw_buf = cl.Buffer(p.ctx, p.mf.WRITE_ONLY, bw_np.nbytes)

    rg_np = np.full((request_size[1], request_size[0], 1), 127, dtype=np.uint8)
    rg_buf = cl.Buffer(p.ctx, p.mf.WRITE_ONLY, rg_np.nbytes)

    gr_np = np.full((request_size[1], request_size[0], 1), 127, dtype=np.uint8)
    gr_buf = cl.Buffer(p.ctx, p.mf.WRITE_ONLY, rg_np.nbytes)

    orient_np = np.full((request_size[1], request_size[0], 4), 127, dtype=np.uint8)
    orient_buf = cl.Buffer(p.ctx, p.mf.WRITE_ONLY, orient_np.nbytes)

    orient_group_np = np.full((request_size[1], request_size[0], 4), 127, dtype=np.uint8)
    orient_group_buf = cl.Buffer(p.ctx, p.mf.WRITE_ONLY, orient_group_np.nbytes)

    end_stop_np = np.full((request_size[1], request_size[0], 8), 127, dtype=np.uint8)
    end_stop_buf = cl.Buffer(p.ctx, p.mf.WRITE_ONLY, end_stop_np.nbytes)

    orient_dbg_np = np.full((request_size[1], request_size[0], 3), 127, dtype=np.uint8)
    orient_dbg_buf = cl.Buffer(p.ctx, p.mf.WRITE_ONLY, orient_dbg_np.nbytes)


    def gpu_main_update(frame  # type: np.ndarray
                        ):
        color = rgc_cb(frame)[0]
        in_buf = cl.Buffer(p.ctx, p.mf.READ_ONLY | p.mf.COPY_HOST_PTR, hostbuf=color)

        time32 = (time.time() * 1000) % (2 ** 32)

        p.build.blob(
            p.queue,
            (request_size[1], request_size[0]),
            (8, 8),
            in_buf,
                     np.uint32(time32),
            by_buf,
            yb_buf,
            bw_buf,
            rg_buf,
            gr_buf,
            orient_buf,
            orient_group_buf,
            end_stop_buf,
            orient_dbg_buf,
                     )

        cl.enqueue_copy(p.queue, by_np, by_buf).wait()
        cl.enqueue_copy(p.queue, yb_np, yb_buf).wait()
        cl.enqueue_copy(p.queue, bw_np, bw_buf).wait()
        cl.enqueue_copy(p.queue, rg_np, rg_buf).wait()
        cl.enqueue_copy(p.queue, gr_np, gr_buf).wait()
        cl.enqueue_copy(p.queue, orient_np, orient_buf).wait()
        cl.enqueue_copy(p.queue, orient_group_np, orient_group_buf).wait()
        cl.enqueue_copy(p.queue, end_stop_np, end_stop_buf).wait()
        cl.enqueue_copy(p.queue, orient_dbg_np, orient_dbg_buf).wait()

        cv2.cvtColor(orient_dbg_np, cv2.COLOR_HSV2BGR, dst=orient_dbg_np)

        return [ by_np, yb_np, bw_np, rg_np, gr_np, orient_dbg_np
                ]

    return gpu_main_update