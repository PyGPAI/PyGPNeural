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

def readCLFile(shaderFile):
    cl_str = ''
    with open(shaderFile) as rgc:
        cl_str = rgc.read()
    return cl_str

def compileRGC(
        shaderFile= my_dir + os.sep + 'retinal shaders'+ os.sep+ 'x-ganglion midget filter combined.cl',
        requestSize=(1280, 720),  # type: Tuple[int, int]
        gpu=None
    ):
    colors = 3

    cl_str = readCLFile(shaderFile).format(requestSize[0], requestSize[1], colors, 127)

    if gpu is None:
        gpus = get_all_cl_gpus()  # get last gpu (typically dedicated one on devices with multiple)
        gpu = [gpus[0]]

    ctx = cl.Context(gpu)
    queue = cl.CommandQueue(ctx)
    mf = cl.mem_flags
    prog = cl.Program(ctx, cl_str).build()

    return (prog, queue, mf, ctx)

allCallbacks = []

def runRGC(
            requestSize=(1280, 720),  # type: Tuple[int, int]

           ):

    global allCallbacks

    prog, queue, mf, ctx = compileRGC(requestSize=requestSize)

    out_np = np.zeros((requestSize[1], requestSize[0]), dtype=np.uint8)
    out_buf = cl.Buffer(ctx, mf.WRITE_ONLY, out_np.nbytes)

    def gpuMainUpdate(frame # type: np.ndarray
                      ):
        in_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=frame)

        prog.rgc(queue, (requestSize[1],requestSize[0],3), None, in_buf, out_buf)

        cl.enqueue_copy(queue, out_np, out_buf).wait()

        return out_np

    allCallbacks.append(gpuMainUpdate)

def DisplayRGC(cam):
    from cv_pubsubs.cv_window_sub import frameDict, cv_win_sub

    runRGC()

    cam = 0

    def camHandler(frame, camId):
        frameDict[str(camId) + "Frame"] = frame

    t = cv_webcam_pub.init_cv_cam_pub_handler(cam, camHandler)

    cv_win_sub(names=[str(cam)],
               inputVidGlobalNames=[str(cam)+'Frame'],
               callbacks=allCallbacks)

    return t

if __name__ == '__main__':
    t = DisplayRGC(0)
    t.join()
