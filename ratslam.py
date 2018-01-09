import numpy as np
import pyopencl as cl
import pubsub

"""def read_in_file(*shader_file):
    '''shader_file = open(script_dir+os.sep+os.sep.join(shader_file))
    shader_text = shader_file.read()
    shader_file.close()'''

    return shader_text"""

import os

my_dir = os.path.dirname(os.path.abspath(__file__))

from cv_pubsubs import cv_webcam_pub, cv_window_sub


def get_all_cl_gpus():
    gpu_list = []
    for platf in cl.get_platforms():
        gpu_list.extend(platf.get_devices(cl.device_type.GPU))

    return gpu_list


if __name__ == '__main__':

    width = 640
    height = 480
    colors = 3

    cl_str = ''
    with open(my_dir + os.sep + 'naive_rgc.cl') as rgc:
        cl_str = rgc.read()

    cl_str = cl_str.format(width, height, colors, 127)

    gpu = get_all_cl_gpus()[-1]  # get last gpu (typically dedicated one on devices with multiple)

    ctx = cl.Context([gpu])

    queue = cl.CommandQueue(ctx)

    mf = cl.mem_flags

    prog = cl.Program(ctx, cl_str).build()

    from cv_pubsubs.cv_window_sub import frameDict, cv_win_sub


    def camHandler(frame, camId):
        frameDict[str(camId) + "Frame"] = frame


    from scipy.ndimage.filters import gaussian_filter

    out_np = np.zeros((height, width, colors), dtype=np.uint32)
    out_buf = cl.Buffer(ctx, mf.WRITE_ONLY, out_np.nbytes)

    def gpuMainUpdate(frame # type: np.ndarray
                      ):
        global prog, outFrame, queue, out_buf, out_np

        in_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=frame.astype(np.uint32))

        prog.rgc(queue, (height,width,colors), None, in_buf, out_buf)

        cl.enqueue_copy(queue, out_np, out_buf).wait()

        return out_np.astype(np.uint8)

    t = cv_webcam_pub.init_cv_cam_pub_handler(0, camHandler)

    cv_win_sub(names=['0'],
               inputVidGlobalNames=['0Frame'],
               callbacks=[gpuMainUpdate])

    t.join()

