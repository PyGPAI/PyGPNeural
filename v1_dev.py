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

    p2 = v1_program(request_size=(request_size[0]/2, request_size[1]/2),
                   gpu=gpu)
    p4 = v1_program(request_size=(request_size[0] / 4, request_size[1] / 4),
                    gpu=gpu)
    p8 = v1_program(request_size=(request_size[0] / 8, request_size[1] / 8),
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

    orient_dbg_np = np.full((request_size[1], request_size[0], 3), 127, dtype=np.uint8)
    orient_dbg_buf = cl.Buffer(p.ctx, p.mf.WRITE_ONLY, orient_dbg_np.nbytes)




    by_np2 = np.full((int(request_size[1]/2), int(request_size[0]/2), 1), 127, dtype=np.uint8)
    by_buf2 = cl.Buffer(p2.ctx, p2.mf.WRITE_ONLY, by_np2.nbytes)
    yb_np2 = np.full((int(request_size[1]/2), int(request_size[0]/2), 1), 127, dtype=np.uint8)
    yb_buf2 = cl.Buffer(p2.ctx, p2.mf.WRITE_ONLY, yb_np2.nbytes)
    bw_np2 = np.full((int(request_size[1]/2), int(request_size[0]/2), 1), 127, dtype=np.uint8)
    bw_buf2 = cl.Buffer(p2.ctx, p2.mf.WRITE_ONLY, bw_np2.nbytes)
    rg_np2 = np.full((int(request_size[1]/2), int(request_size[0]/2), 1), 127, dtype=np.uint8)
    rg_buf2 = cl.Buffer(p2.ctx, p2.mf.WRITE_ONLY, rg_np2.nbytes)
    gr_np2 = np.full((int(request_size[1]/2), int(request_size[0]/2), 1), 127, dtype=np.uint8)
    gr_buf2 = cl.Buffer(p2.ctx, p2.mf.WRITE_ONLY, rg_np2.nbytes)
    orient_np2 = np.full((int(request_size[1]/2), int(request_size[0]/2), 4), 127, dtype=np.int16)
    orient_buf2 = cl.Buffer(p2.ctx, p2.mf.WRITE_ONLY, orient_np2.nbytes)
    orient_dbg_np2 = np.full((int(request_size[1]/2), int(request_size[0]/2), 3), 127, dtype=np.uint8)
    orient_dbg_buf2 = cl.Buffer(p2.ctx, p2.mf.WRITE_ONLY, orient_dbg_np2.nbytes)

    by_np4 = np.full((int(request_size[1] / 4), int(request_size[0] / 4), 1), 127, dtype=np.uint8)
    by_buf4 = cl.Buffer(p4.ctx, p4.mf.WRITE_ONLY, by_np4.nbytes)
    yb_np4 = np.full((int(request_size[1] / 4), int(request_size[0] / 4), 1), 127, dtype=np.uint8)
    yb_buf4 = cl.Buffer(p4.ctx, p4.mf.WRITE_ONLY, yb_np4.nbytes)
    bw_np4 = np.full((int(request_size[1] / 4), int(request_size[0] / 4), 1), 127, dtype=np.uint8)
    bw_buf4 = cl.Buffer(p4.ctx, p4.mf.WRITE_ONLY, bw_np4.nbytes)
    rg_np4 = np.full((int(request_size[1] / 4), int(request_size[0] / 4), 1), 127, dtype=np.uint8)
    rg_buf4 = cl.Buffer(p4.ctx, p4.mf.WRITE_ONLY, rg_np4.nbytes)
    gr_np4 = np.full((int(request_size[1] / 4), int(request_size[0] / 4), 1), 127, dtype=np.uint8)
    gr_buf4 = cl.Buffer(p4.ctx, p4.mf.WRITE_ONLY, rg_np4.nbytes)
    orient_np4 = np.full((int(request_size[1] / 4), int(request_size[0] / 4), 4), 127, dtype=np.int16)
    orient_buf4 = cl.Buffer(p4.ctx, p4.mf.WRITE_ONLY, orient_np4.nbytes)
    orient_dbg_np4 = np.full((int(request_size[1] / 4), int(request_size[0] / 4), 3), 127, dtype=np.uint8)
    orient_dbg_buf4 = cl.Buffer(p4.ctx, p4.mf.WRITE_ONLY, orient_dbg_np4.nbytes)

    by_np8 = np.full((int(request_size[1] / 8), int(request_size[0] / 8), 1), 127, dtype=np.uint8)
    by_buf8 = cl.Buffer(p8.ctx, p8.mf.WRITE_ONLY, by_np8.nbytes)
    yb_np8 = np.full((int(request_size[1] / 8), int(request_size[0] / 8), 1), 127, dtype=np.uint8)
    yb_buf8 = cl.Buffer(p8.ctx, p8.mf.WRITE_ONLY, yb_np8.nbytes)
    bw_np8 = np.full((int(request_size[1] / 8), int(request_size[0] / 8), 1), 127, dtype=np.uint8)
    bw_buf8 = cl.Buffer(p8.ctx, p8.mf.WRITE_ONLY, bw_np8.nbytes)
    rg_np8 = np.full((int(request_size[1] / 8), int(request_size[0] / 8), 1), 127, dtype=np.uint8)
    rg_buf8 = cl.Buffer(p8.ctx, p8.mf.WRITE_ONLY, rg_np8.nbytes)
    gr_np8 = np.full((int(request_size[1] / 8), int(request_size[0] / 8), 1), 127, dtype=np.uint8)
    gr_buf8 = cl.Buffer(p8.ctx, p8.mf.WRITE_ONLY, rg_np8.nbytes)
    orient_np8 = np.full((int(request_size[1] / 8), int(request_size[0] / 8), 4), 127, dtype=np.int16)
    orient_buf8 = cl.Buffer(p8.ctx, p8.mf.WRITE_ONLY, orient_np8.nbytes)
    orient_dbg_np8 = np.full((int(request_size[1] / 8), int(request_size[0] / 8), 3), 127, dtype=np.uint8)
    orient_dbg_buf8 = cl.Buffer(p8.ctx, p8.mf.WRITE_ONLY, orient_dbg_np8.nbytes)

    def gpu_main_update(frame  # type: np.ndarray
                        ):
        color = rgc_cb(frame)[0]
        color2 = cv2.resize(color, (0,0), fx=0.5,fy=0.5)
        color4 = cv2.resize(color2, (0, 0), fx=0.5, fy=0.5)
        color8 = cv2.resize(color4, (0, 0), fx=0.5, fy=0.5)
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
            orient_dbg_buf,
                     )

        cl.enqueue_copy(p.queue, by_np, by_buf).wait()
        cl.enqueue_copy(p.queue, yb_np, yb_buf).wait()
        cl.enqueue_copy(p.queue, bw_np, bw_buf).wait()
        cl.enqueue_copy(p.queue, rg_np, rg_buf).wait()
        cl.enqueue_copy(p.queue, gr_np, gr_buf).wait()
        cl.enqueue_copy(p.queue, orient_np, orient_buf).wait()
        cl.enqueue_copy(p.queue, orient_dbg_np, orient_dbg_buf).wait()

        cv2.cvtColor(orient_dbg_np, cv2.COLOR_HSV2BGR, dst=orient_dbg_np)





        in_buf2 = cl.Buffer(p2.ctx, p2.mf.READ_ONLY | p2.mf.COPY_HOST_PTR, hostbuf=color2)

        time32 = (time.time() * 1000) % (2 ** 32)

        p2.build.blob(
            p2.queue,
            (int(request_size[1]/2), int(request_size[0]/2)),
            (8, 8),
            in_buf2,
            np.uint32(time32),
            by_buf2,
            yb_buf2,
            bw_buf2,
            rg_buf2,
            gr_buf2,
            orient_buf2,
            orient_dbg_buf2,
        )

        cl.enqueue_copy(p2.queue, by_np2, by_buf2).wait()
        cl.enqueue_copy(p2.queue, yb_np2, yb_buf2).wait()
        cl.enqueue_copy(p2.queue, bw_np2, bw_buf2).wait()
        cl.enqueue_copy(p2.queue, rg_np2, rg_buf2).wait()
        cl.enqueue_copy(p2.queue, gr_np2, gr_buf2).wait()
        cl.enqueue_copy(p2.queue, orient_np2, orient_buf2).wait()
        cl.enqueue_copy(p2.queue, orient_dbg_np2, orient_dbg_buf2).wait()

        cv2.cvtColor(orient_dbg_np2, cv2.COLOR_HSV2BGR, dst=orient_dbg_np2)



        in_buf4 = cl.Buffer(p4.ctx, p4.mf.READ_ONLY | p4.mf.COPY_HOST_PTR, hostbuf=color4)
        time34 = (time.time() * 1000) % (2 ** 32)
        p4.build.blob(
            p4.queue,
            (int(request_size[1] / 4), int(request_size[0] / 4)),
            (8, 8),
            in_buf4,
            np.uint32(time34),
            by_buf4,
            yb_buf4,
            bw_buf4,
            rg_buf4,
            gr_buf4,
            orient_buf4,
            orient_dbg_buf4,
        )
        cl.enqueue_copy(p4.queue, by_np4, by_buf4).wait()
        cl.enqueue_copy(p4.queue, yb_np4, yb_buf4).wait()
        cl.enqueue_copy(p4.queue, bw_np4, bw_buf4).wait()
        cl.enqueue_copy(p4.queue, rg_np4, rg_buf4).wait()
        cl.enqueue_copy(p4.queue, gr_np4, gr_buf4).wait()
        cl.enqueue_copy(p4.queue, orient_np4, orient_buf4).wait()
        cl.enqueue_copy(p4.queue, orient_dbg_np4, orient_dbg_buf4).wait()
        cv2.cvtColor(orient_dbg_np4, cv2.COLOR_HSV2BGR, dst=orient_dbg_np4)

        in_buf8 = cl.Buffer(p8.ctx, p8.mf.READ_ONLY | p8.mf.COPY_HOST_PTR, hostbuf=color8)
        time38 = (time.time() * 1000) % (2 ** 32)
        p8.build.blob(
            p8.queue,
            (int(request_size[1] / 8), int(request_size[0] / 8)),
            (6, 8),
            in_buf8,
            np.uint32(time38),
            by_buf8,
            yb_buf8,
            bw_buf8,
            rg_buf8,
            gr_buf8,
            orient_buf8,
            orient_dbg_buf8,
        )
        cl.enqueue_copy(p8.queue, by_np8, by_buf8).wait()
        cl.enqueue_copy(p8.queue, yb_np8, yb_buf8).wait()
        cl.enqueue_copy(p8.queue, bw_np8, bw_buf8).wait()
        cl.enqueue_copy(p8.queue, rg_np8, rg_buf8).wait()
        cl.enqueue_copy(p8.queue, gr_np8, gr_buf8).wait()
        cl.enqueue_copy(p8.queue, orient_np8, orient_buf8).wait()
        cl.enqueue_copy(p8.queue, orient_dbg_np8, orient_dbg_buf8).wait()
        cv2.cvtColor(orient_dbg_np8, cv2.COLOR_HSV2BGR, dst=orient_dbg_np8)

        return [orient_dbg_np,
                orient_dbg_np2,
                orient_dbg_np4,
                orient_dbg_np8
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

    win.sub_win_loop(names=['orient_dbg_np',
                            'orient_dbg_np2',
                            'orient_dbg_np4',
                            'orient_dbg_np8',
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