import os
import numpy as np
import pyopencl as cl
import time

import math as m
import cv2

import pygp_util as pgpu
from .shader_util import shader_dir as rgc_shader_dir

if False:
    from typing import Optional, List, Tuple, Union

class RGCBundle:
    num_scales = 0
    scaled_frames = []
    scaled_edges = []
    scaled_color_edges = []
    scaled_time_frames = []

#todo: all multiple scale creation should be done in one GPU run
class RGC( object ):

    @staticmethod
    def get_size_list(original_size = (640, 480),
                      min_size = (100,100),
                      x_scale_divisor = m.sqrt(2),
                      y_scale_divisor = None,

                      ):
        size_list = []
        current_size = list(original_size)

        if y_scale_divisor is None:
            y_scale_divisor = x_scale_divisor

        while current_size[0]>min_size[0] and current_size[1]>min_size[1]:
            size_list.append(current_size[:])
            current_size[0]=int(round(current_size[0]/x_scale_divisor))
            current_size[1]=int(round(current_size[1]/y_scale_divisor))
            if current_size==size_list[-1]:
                break
        return size_list

    @staticmethod
    def check_size_list(size_list):
        if not isinstance(size_list, list) and len(size_list)>0 and len(size_list[0])!=2:
            raise ValueError("Incorrect size list format. Should be [[x1,y1], [x2,y2], ...].")

        current_x, current_y = float("inf"), float("inf")

        for size in size_list:
            if size[0]>current_x or size[1]>current_y:
                raise ValueError("widths and heights in size list must be in non-increasing order.")
            else:
                current_x, current_y = size[0], size[1]
        return size_list

    def __init__(self,
                 request_sizes=None,  # type: Optional[List[Union[List[int, int], Tuple[int,int]]]]
                 relative_color_filter=True,
                 edge_filter=True,
                 time_filter=False,
                 combine_time_and_color=False,
                 gpu=None
                 ):

        if request_sizes is None:
            self.request_sizes = self.get_size_list()
        else:
            self.request_sizes = self.check_size_list(request_sizes)

        self.is_computing_relative_color_filter = relative_color_filter
        self.is_computing_edge_filter = edge_filter
        self.is_computing_time_filter = time_filter
        self.combine_time_and_color = combine_time_and_color
        self.gpu = gpu

        self.displaying = False


    def make_program(self):
        cl_str = pgpu.format_read_file(shader_file=rgc_shader_dir + os.sep + 'RetinalGanglianFilter.cl',
                                       format_args=()
                                       )

        shady_p = pgpu.ShaderProgram(self.gpu)

        options = [r"-I", pgpu.shader_dir]
        if self.is_computing_relative_color_filter:
            options.extend(["-D", "RELATIVE_COLOR_FILTER"])
            if self.combine_time_and_color:
                options.extend(["-D", "RELATIVE_TIME_FILTER"])
        if self.is_computing_edge_filter:
            options.extend(["-D", "EDGE_FILTER"])
        if self.is_computing_time_filter:
            options.extend(["-D", "TIME_FILTER"])

        shady_p.build_program(cl_str, options)

        return shady_p

    def rgc_nocl_callback(self):
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

    def setup_callback(self,
                       expected_colors = None):
        self.p = self.make_program()

        if expected_colors is None:
            expected_colors = 3

        self.scaled_videos_np = []  # type: List[np.ndarray]
        self.scaled_videos_buf = [] # type: List[np.ndarray]

        self.scaled_color_edge_filters_np = []  # type: List[np.ndarray]
        self.scaled_color_edge_filters_buf = []  # type: List[np.ndarray]

        self.scaled_edge_filters_np = []  # type: List[np.ndarray]
        self.scaled_edge_filters_buf = []  # type: List[np.ndarray]

        self.scaled_time_filters_np = []  # type: List[np.ndarray]
        self.scaled_time_filters_buf = []  # type: List[np.ndarray]

        for size in self.request_sizes:
            self.scaled_videos_np.append(
                np.full((size[1],size[0], expected_colors), 127, dtype=np.uint8)
            )
            self.scaled_videos_buf.append(
                cl.Buffer(self.p.ctx, self.p.mf.WRITE_ONLY, self.scaled_videos_np[-1].nbytes)
            )

            if self.is_computing_relative_color_filter:
                self.scaled_color_edge_filters_np.append(
                    np.full((size[1], size[0], expected_colors), 127, dtype=np.uint8)
                )
                self.scaled_color_edge_filters_buf.append(
                    cl.Buffer(self.p.ctx, self.p.mf.WRITE_ONLY, self.scaled_color_edge_filters_np[-1].nbytes)
                )

            if self.is_computing_edge_filter:
                self.scaled_edge_filters_np.append(
                    np.full((size[1], size[0], 1), 127, dtype=np.uint8)
                )
                self.scaled_edge_filters_buf.append(
                    cl.Buffer(self.p.ctx, self.p.mf.WRITE_ONLY, self.scaled_edge_filters_np[-1].nbytes)
                )

            if self.is_computing_time_filter:
                self.scaled_time_filters_np.append(
                    np.full((size[1], size[0], expected_colors), 127, dtype=np.uint8)
                )
                self.scaled_time_filters_buf.append(
                    cl.Buffer(self.p.ctx, self.p.mf.WRITE_ONLY, self.scaled_time_filters_np[-1].nbytes)
                )

        return self.main_callback

    def main_callback(self,
                      frame  # type: np.ndarray
                        ):

        prev_size = [frame.shape[1], frame.shape[0]]
        num_colors = frame.shape[2]

        #todo: use try-except, and then update with this if fails in certain way
        #if self.scaled_videos_np[0].shape[2]!=num_colors:
        #    self.setup_callback(num_colors)

        for i in range(len(self.request_sizes)):

            in_buf = cl.Buffer(self.p.ctx, self.p.mf.READ_ONLY | self.p.mf.COPY_HOST_PTR, hostbuf=frame)

            args = [
                self.p.queue, (self.request_sizes[i][1], self.request_sizes[i][0], num_colors), (1, 1, 1),
                np.uint32(prev_size[1]), np.uint32(prev_size[0]), np.uint32(self.request_sizes[i][1]), np.uint32(self.request_sizes[i][0]), np.uint32(num_colors),
                in_buf]

            buffs = [self.scaled_videos_buf[i]]
            if self.is_computing_relative_color_filter:
                buffs.append(self.scaled_color_edge_filters_buf[i])
            if self.is_computing_edge_filter:
                buffs.append(self.scaled_edge_filters_buf[i])
            if self.is_computing_time_filter:
                buffs.append(self.scaled_time_filters_buf[i])
            args.extend(buffs)

            self.p.build.rgc(*args)

            arrays = [self.scaled_videos_np[i]]
            if self.is_computing_relative_color_filter:
                arrays.append(self.scaled_color_edge_filters_np[i])
            if self.is_computing_edge_filter:
                arrays.append(self.scaled_edge_filters_np[i])
            if self.is_computing_time_filter:
                arrays.append(self.scaled_time_filters_np[i])

            for b in range(len(buffs)):
                cl.enqueue_copy(self.p.queue, arrays[b], buffs[b]).wait()

            frame = arrays[0]

            prev_size = self.request_sizes[i]

        arrays = [vid for vid in self.scaled_videos_np]
        if self.is_computing_relative_color_filter:
            arrays.extend([color_edge for color_edge in self.scaled_color_edge_filters_np])
        if self.is_computing_edge_filter:
            arrays.extend([edge for edge in self.scaled_edge_filters_np])
        if self.is_computing_time_filter:
            arrays.extend([t for t in self.scaled_time_filters_np])

        if self.displaying:
            return arrays

    @property
    def current_bundle(self):  # type: ()->RGCBundle
        bun = RGCBundle()

        bun.num_scales= len(self.request_sizes)

        bun.scaled_frames = [vid for vid in self.scaled_videos_np]

        if self.is_computing_relative_color_filter:
            bun.scaled_color_edges = [color_edge for color_edge in self.scaled_color_edge_filters_np]
        if self.is_computing_edge_filter:
            bun.scaled_edges = [edge for edge in self.scaled_edge_filters_np]
        if self.is_computing_time_filter:
            bun.scaled_time_frames = [t for t in self.scaled_time_filters_np]

        return bun


