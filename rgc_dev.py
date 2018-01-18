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
        relative_color_filter = True,
        edge_filter = True,
        average_color_filter = True,
        shaderFile= None,
        requestSize=(1280, 720),  # type: Tuple[int, int]
        gpu=None
    ):
    colors = 3
    if shaderFile is None:
            shaderFile = my_dir + os.sep + 'retinal shaders' + os.sep + 'RetinalGanglianFilter.cl'
    cl_str = readCLFile(shaderFile).format(requestSize[0], requestSize[1], colors, 127)

    if gpu is None:
        gpus = get_all_cl_gpus()  # get last gpu (typically dedicated one on devices with multiple)
        gpu = [gpus[0]]

    ctx = cl.Context(gpu)
    queue = cl.CommandQueue(ctx)
    mf = cl.mem_flags

    options = [r"-I", my_dir + os.sep + 'retinal shaders']
    if relative_color_filter:
        options.extend(["-D", "RELATIVE_COLOR_FILTER"])
    if edge_filter:
        options.extend(["-D", "EDGE_FILTER"])
    if average_color_filter:
        options.extend(["-D", "AVG_COLOR"])


    prog = cl.Program(ctx, cl_str).build(options=options)

    return (prog, queue, mf, ctx)

allCallbacks = []

import time
def runRGC(
            requestSize=(1280, 720),  # type: Tuple[int, int]
            relative_color_filter=True,
            edge_filter=True,
            average_color_filter=True
           ):

    global allCallbacks

    prog, queue, mf, ctx = compileRGC(
        relative_color_filter=relative_color_filter,
        edge_filter=edge_filter,
        average_color_filter=average_color_filter,
        requestSize=requestSize)

    if relative_color_filter:
        color_np = np.zeros((requestSize[1], requestSize[0], 3), dtype=np.uint8)
        color_buf = cl.Buffer(ctx, mf.WRITE_ONLY, color_np.nbytes)

    if edge_filter:
        edge_np = np.zeros((requestSize[1], requestSize[0], 1), dtype=np.uint8)
        edge_buf = cl.Buffer(ctx, mf.WRITE_ONLY, edge_np.nbytes)

    if average_color_filter:
        avg_np = np.zeros((1,1,3,), dtype=np.uint8)
        avg_buf = cl.Buffer(ctx, mf.WRITE_ONLY, avg_np.nbytes)

    def gpuMainUpdate(frame # type: np.ndarray
                      ):
        in_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=frame)

        time32 = (time.time() * 1000) % (2 ** 32)
        args = [queue, (requestSize[1],requestSize[0],3), (8,8,1), in_buf, np.uint32(time32)]

        buffs = []
        if relative_color_filter:
            buffs.append(color_buf)
        if edge_filter:
            buffs.append(edge_buf)
        if average_color_filter:
            buffs.append(avg_buf)
        args.extend(buffs)

        prog.rgc(*args)

        arrays = []
        if relative_color_filter:
            arrays.append(color_np)
        if edge_filter:
            arrays.append(edge_np)
        if average_color_filter:
            arrays.append(avg_np)

        for b in range(len(buffs)):
            cl.enqueue_copy(queue, arrays[b], buffs[b] ).wait()

        if average_color_filter:
            print(avg_np)

        return arrays

    allCallbacks.append(gpuMainUpdate)

def DisplayRGC(cam,
               requestSize=(1280, 720),  # type: Tuple[int, int]
               ):
    from cv_pubsubs.cv_window_sub import frameDict, cv_win_sub

    runRGC(requestSize)


    def camHandler(frame, camId):
        frameDict[str(camId) + "Frame"] = frame

    t = cv_webcam_pub.init_cv_cam_pub_handler(cam, camHandler)

    cv_win_sub(names=[str(cam)],
               inputVidGlobalNames=[str(cam)+'Frame'],
               callbacks=allCallbacks)

    return t

if __name__ == '__main__':
    t = DisplayRGC(0, (1280,720))
    t.join()
