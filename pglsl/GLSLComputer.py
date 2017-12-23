import ModernGL
import re

class GLSLComputer(object):
    def __init__(self, compute_shader, **named_args):
        self.ctx = ModernGL.create_standalone_context()

        #self.prog = self.ctx.program([self.ctx.compute_shader(compute_shader)])

        self.cpu = self.ctx.compute_shader(compute_shader)

        #self.cpu.uniform_blocks['Output'].
        for name, value in named_args.items():
            self.cpu.uniforms[name].value = value
