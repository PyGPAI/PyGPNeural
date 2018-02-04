import os
os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1'

my_dir = os.path.dirname(os.path.abspath(__file__))

shader_dir = my_dir + os.sep + 'v1 shaders'