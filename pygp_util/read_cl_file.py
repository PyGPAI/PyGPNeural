
def read_file(shader_file):
    with open(shader_file) as f:
        cl_str = f.read()
    return cl_str

def format_read_file(*, shader_file, format_args, format_dict=None):
    if format_dict is not None:
        return read_file(shader_file).format(*format_args, **format_dict)
    else:
        return read_file(shader_file).format(*format_args)
