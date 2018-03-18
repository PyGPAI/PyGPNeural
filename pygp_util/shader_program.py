import pyopencl as cl
from .get_nth_device import get_nth_gpu
from .get_nth_device import get_nth_cpu
class ShaderProgram(object):
    def __init__(self, gpu=None):
        if gpu is None or isinstance(gpu, int):
            try:
                gpu = get_nth_gpu(gpu)
            except IndexError:
                try:
                    gpu = get_nth_gpu(None)
                except IndexError:
                    gpu = get_nth_cpu(None)

        self.gpu = gpu
        self.ctx = cl.Context([gpu])
        self.queue = cl.CommandQueue(self.ctx)
        self.mf = cl.mem_flags

    def build_program(self, cl_str, options):
        self.prog = cl.Program(self.ctx, cl_str)
        self.build = self.prog.build(options=options)
        return self.build
