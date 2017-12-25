from pglsl_cpu import GLSLComputer
import numpy as np
import pubsub

"""def read_in_file(*shader_file):
    '''shader_file = open(script_dir+os.sep+os.sep.join(shader_file))
    shader_text = shader_file.read()
    shader_file.close()'''

    return shader_text"""

import os
my_dir = os.path.dirname(os.path.abspath(__file__))

from cv_pubsubs import cv_webcam_pub, cv_window_sub

if __name__ == '__main__':
    shad_str = ''
    with open(my_dir+os.sep+'rgc.glsl') as rgc:
        shad_str = rgc.read()

    width=640
    height = 480
    colors = 3
    gpu = GLSLComputer.GLSLComputer(shad_str,
                                    width=width, height=height, colors=colors,
                                    whichBuffer=0)
    buff = gpu.ctx.buffer(data=np.zeros(width * height * colors).astype(dtype=np.float32).tobytes())
    buff.bind_to_storage_buffer(0)

    buff2 = gpu.ctx.buffer(data=np.zeros(width * height * colors).astype(dtype=np.float32).tobytes())
    buff2.bind_to_storage_buffer(1)

    from cv_pubsubs.cv_window_sub import frameDict, cv_win_sub

    def camHandler(frame, camId):
        frameDict[str(camId)+"Frame"]= frame

    from scipy.ndimage.filters import gaussian_filter

    storeFrame = np.zeros(width * height * colors).astype(dtype=np.float32).reshape(height, width, colors)

    def gpuMainUpdate(frame):
        global storeFrame
        if gpu.cpu.uniforms['whichBuffer'].value == 0:
            prevGot = np.frombuffer(buff.read(), dtype=np.float32).reshape(height, width, colors)
            frameOut = prevGot
            storeFrame = gaussian_filter(np.clip((storeFrame + prevGot)/1.9, 0,255),3)
            buff.write(np.clip(frame+storeFrame, 0,255).astype(dtype=np.float32).tobytes())

        else:
            prevGot = np.frombuffer(buff2.read(), dtype=np.float32).reshape(height, width, colors)
            frameOut = prevGot
            storeFrame = gaussian_filter(np.clip((storeFrame + prevGot)/1.9, 0,255),3)
            buff2.write(np.clip(frame+storeFrame, 0,255).astype(dtype=np.float32).tobytes())

        gpu.cpu.run(width, height, colors)
        if gpu.cpu.uniforms['whichBuffer'].value == 0:
            gpu.cpu.uniforms['whichBuffer'].value = 1
        else:
            gpu.cpu.uniforms['whichBuffer'].value = 0
        return frameOut/255


    t = cv_webcam_pub.init_cv_cam_pub_handler(0,camHandler)

    cv_win_sub(names=['cammy'], inputVidGlobalNames=['0Frame'], callbacks=[gpuMainUpdate])

    pubsub.publish("cvcamhandlers.0.cmd", 'q')
    t.join()
