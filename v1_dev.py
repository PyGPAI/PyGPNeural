from pygp_retina.rgc import rgc_callback
import cv2
import os
import pyopencl as cl
import pygp_util as pgpu
from shader_util import shader_dir as v1_shader_dir
import time

import numpy as np
if False:
    from typing import Tuple

def v1_program(
               request_size=(1280,720),
               gpu=None
               ):
    cl_str = pgpu.format_read_file(shader_file=v1_shader_dir + os.sep + 'blob shader.cl',
                                   format_args=(request_size[0], request_size[1], "(int3)(127,127,127)"))

    shady_p = pgpu.ShaderProgram(gpu)

    options = [r"-I", pgpu.shader_dir]

    shady_p.build_program(cl_str, options)

    return shady_p


def col_mask_callback(
        request_size=(1280, 720),  # type: Tuple[int, int]
        gpu=None
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

    orient_np = np.full((request_size[1], request_size[0], 4), 127, dtype=np.int16)
    orient_buf = cl.Buffer(p.ctx, p.mf.WRITE_ONLY, orient_np.nbytes)

    orient_group_np = np.full((request_size[1], request_size[0], 4), 127, dtype=np.int16)
    orient_group_buf = cl.Buffer(p.ctx, p.mf.WRITE_ONLY, orient_group_np.nbytes)

    end_stop_np = np.full((request_size[1], request_size[0], 4), 127, dtype=np.int16)
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

        return [orient_dbg_np
                ]

    return gpu_main_update

from cv_pubsubs import webcam_pub as camp
from cv_pubsubs import window_sub as win

from pygp_retina import rgc_callback

if False:
    from typing import Tuple

def display_col_mask(cam,
                    request_size=(1280, 720),  # type: Tuple[int, int]
                    fps_limit=60  # type: float
                ):
    def cam_handler(frame, cam_id):
        win.frame_dict[str(cam_id) + "Frame"] = frame

    cam_thread = camp.frame_handler_thread(cam, cam_handler, fps_limit=fps_limit,
                                           high_speed=True)

    win.sub_win_loop(names=['orient_dbg_np'
                            ],
                     input_cams=[cam],
                     input_vid_global_names=[str(cam) + 'Frame'],
                     callbacks=[col_mask_callback(request_size,
                                             gpu = 0
    )])

    return cam_thread

if __name__=='__main__':
    t = display_col_mask(cam=0,
                    request_size=(640, 480),
                    fps_limit=60)

    t.join()
