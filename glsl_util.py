import re
import os

def glsl_import_filter(shader_str, include_dir):
    include_re = re.compile("#include\s*\"([a-zA-Z0-9\.]+)\"")

    includes = include_re.finditer(shader_str)
    for i in includes:
        shader_file = open(include_dir+os.sep+i.group(1))
        addon_shader = shader_file.read()
        shader_file.close()

        shader_str_start = shader_str[0:i.span()[0]]
        shader_str_end = shader_str[i.span()[1]:]

        shader_str = shader_str_start+addon_shader+shader_str_end

    return shader_str