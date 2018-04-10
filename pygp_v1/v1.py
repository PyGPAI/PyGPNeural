import cv2
import os
import pyopencl as cl
import pygp_util as pgpu
from .shader_util import shader_dir as v1_shader_dir
import time

import math as m

import numpy as np
if False:
    from typing import Tuple, List

from pygp_retina import RGC

class V1Bundle:
    num_scales = 0
    scaled_ybs = []
    scaled_bys = []
    scaled_bws = []
    scaled_rgs = []
    scaled_grs = []
    scaled_orients = []
    scaled_orient_groups = []
    scaled_end_stops = []
    scaled_orient_debugs = []

#todo: all multiple scale handling should be done in one GPU run
class V1( object ):

    def __init__(self,
                 request_sizes = None,
                 gpu = None,
                 rgc = None):
        self.request_sizes = request_sizes
        self.gpu = gpu
        if rgc is not None:
            self.rgc = rgc
            if request_sizes is not None:
                self.rgc.request_sizes = request_sizes
        else:
            self.rgc = RGC(request_sizes,
                           relative_color_filter=True,
                           edge_filter=False,
                           time_filter=False,
                           combine_time_and_color=False,
                           gpu=gpu)

        self.is_displaying=False

    def make_programs(self,
                      ):

        prog_list = []  # type: List[pgpu.ShaderProgram]
        for size in self.request_sizes:
            cl_str = pgpu.format_read_file(shader_file=v1_shader_dir + os.sep + 'v1_shader.cl',
                                           format_args=(size[0], size[1], "(int3)(127,127,127)"))

            shady_p = pgpu.ShaderProgram(self.gpu)

            options = [r"-I", v1_shader_dir , r"-I", pgpu.shader_dir]

            shady_p.build_program(cl_str, options)

            prog_list.append(shady_p)

        return prog_list


    def nocl_callback(self, ):
        rgc_cb = self.rgc.rgc_nocl_callback()

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

    def set_cl_array_list_item(
            self,
            s,  # type: int
            num_colors,  # type: int
            arrays_np,  # type: List[np.ndarray]
            arrays_buf  # type: List[cl.Buffer]
    ):
        arrays_np.append(
            np.full((self.request_sizes[s][1], self.request_sizes[s][0], num_colors), 127, dtype=np.uint8)
        )
        arrays_buf.append(
            cl.Buffer(self.prog_list[s].ctx, self.prog_list[s].mf.WRITE_ONLY, arrays_np[-1].nbytes)
        )


    def setup_callback(self):
        self.rgc.setup_callback()

        self.prog_list = self.make_programs()

        self.scaled_by_nps = []  # type: List[np.ndarray]
        self.scaled_by_bufs = []  # type: List[cl.Buffer]

        self.scaled_yb_nps = []  # type: List[np.ndarray]
        self.scaled_yb_bufs = []  # type: List[cl.Buffer]

        self.scaled_bw_nps = []  # type: List[np.ndarray]
        self.scaled_bw_bufs = []  # type: List[cl.Buffer]

        self.scaled_rg_nps = []  # type: List[np.ndarray]
        self.scaled_rg_bufs = []  # type: List[cl.Buffer]

        self.scaled_gr_nps = []  # type: List[np.ndarray]
        self.scaled_gr_bufs = []  # type: List[cl.Buffer]

        self.scaled_orient_nps = []  # type: List[np.ndarray]
        self.scaled_orient_bufs = []  # type: List[cl.Buffer]

        self.scaled_orient_group_nps = []  # type: List[np.ndarray]
        self.scaled_orient_group_bufs = []  # type: List[cl.Buffer]

        self.scaled_end_stop_nps = []  # type: List[np.ndarray]
        self.scaled_end_stop_bufs = []  # type: List[cl.Buffer]

        self.scaled_orient_debug_nps = []  # type: List[np.ndarray]
        self.scaled_orient_debug_bufs = []  # type: List[cl.Buffer]

        for s in range(len(self.request_sizes)):
            self.set_cl_array_list_item(s, 1, self.scaled_by_nps, self.scaled_by_bufs)
            self.set_cl_array_list_item(s, 1, self.scaled_yb_nps, self.scaled_yb_bufs)
            self.set_cl_array_list_item(s, 1, self.scaled_bw_nps, self.scaled_bw_bufs)
            self.set_cl_array_list_item(s, 1, self.scaled_rg_nps, self.scaled_rg_bufs)
            self.set_cl_array_list_item(s, 1, self.scaled_gr_nps, self.scaled_gr_bufs)
            self.set_cl_array_list_item(s, 4, self.scaled_orient_nps, self.scaled_orient_bufs)
            self.set_cl_array_list_item(s, 4, self.scaled_orient_group_nps, self.scaled_orient_group_bufs)
            self.set_cl_array_list_item(s, 4, self.scaled_end_stop_nps, self.scaled_end_stop_bufs)
            self.set_cl_array_list_item(s, 3, self.scaled_orient_debug_nps, self.scaled_orient_debug_bufs)

    def main_callback(self,
                      frame  # type: np.ndarray
                      ):

        self.rgc.main_callback(frame)

        colors = self.rgc.current_bundle.scaled_color_edges

        for c in range(len(colors)):
            in_buf = cl.Buffer(self.prog_list[c].ctx, self.prog_list[c].mf.READ_ONLY | self.prog_list[c].mf.COPY_HOST_PTR, hostbuf=colors[c])

            time32 = (time.time() * 1000) % (2 ** 32)

            self.prog_list[c].build.blob(
                self.prog_list[c].queue,
                (self.request_sizes[c][1], self.request_sizes[c][0]),
                (1, 1),
                in_buf,
                np.uint32(time32),
                self.scaled_by_bufs[c],
                self.scaled_yb_bufs[c],
                self.scaled_bw_bufs[c],
                self.scaled_rg_bufs[c],
                self.scaled_gr_bufs[c],
                self.scaled_orient_bufs[c],
                self.scaled_orient_group_bufs[c],
                self.scaled_end_stop_bufs[c],
                self.scaled_orient_debug_bufs[c],
                         )

            cl.enqueue_copy(self.prog_list[c].queue, self.scaled_by_nps[c], self.scaled_by_bufs[c]).wait()
            cl.enqueue_copy(self.prog_list[c].queue, self.scaled_yb_nps[c], self.scaled_yb_bufs[c]).wait()
            cl.enqueue_copy(self.prog_list[c].queue, self.scaled_bw_nps[c], self.scaled_bw_bufs[c]).wait()
            cl.enqueue_copy(self.prog_list[c].queue, self.scaled_rg_nps[c], self.scaled_rg_bufs[c]).wait()
            cl.enqueue_copy(self.prog_list[c].queue, self.scaled_gr_nps[c], self.scaled_gr_bufs[c]).wait()
            cl.enqueue_copy(self.prog_list[c].queue, self.scaled_orient_nps[c], self.scaled_orient_bufs[c]).wait()
            cl.enqueue_copy(self.prog_list[c].queue, self.scaled_orient_group_nps[c], self.scaled_orient_group_bufs[c]).wait()
            cl.enqueue_copy(self.prog_list[c].queue, self.scaled_end_stop_nps[c], self.scaled_end_stop_bufs[c]).wait()
            cl.enqueue_copy(self.prog_list[c].queue, self.scaled_orient_debug_nps[c], self.scaled_orient_debug_bufs[c]).wait()

            cv2.cvtColor(self.scaled_orient_debug_nps[c], cv2.COLOR_HSV2BGR, dst=self.scaled_orient_debug_nps[c])

        if self.is_displaying:
            return self.current_bundle.scaled_orient_debugs

    @property
    def current_bundle(self):
        bun = V1Bundle()

        bun.num_scales = len(self.request_sizes)

        bun.scaled_bws = self.scaled_bw_nps
        bun.scaled_bys = self.scaled_by_nps
        bun.scaled_ybs = self.scaled_yb_nps
        bun.scaled_grs = self.scaled_gr_nps
        bun.scaled_rgs = self.scaled_rg_nps

        bun.scaled_orients = self.scaled_orient_nps
        bun.scaled_orient_groups = self.scaled_orient_group_nps
        bun.scaled_end_stops = self.scaled_end_stop_nps

        bun.scaled_orient_debugs = self.scaled_orient_debug_nps

        return bun