#This library contains a few functions not in colorsys

import math as m
import numpy as np
import integer
import numbers

#not actually optimized. Just looks similar to GPU programming, but is for loop.
#this could be done with builtin numpy functions, or GPU stuff
def _np_float_to_char(color_val):
    color_val = integer.minmax(color_val, 0.0, 1.0)
    return color_val*255

_np_float_to_char = np.vectorize(_np_float_to_char, otypes=[np.uint8])

def float_to_char(color_val):
    if isinstance(color_val, (np.ndarray, np.generic)):
        return _np_float_to_char(color_val)
    elif isinstance(color_val, (list, tuple)):
        for i in range(len(color_val)):
            color_val[i] = integer.minmax(color_val, 0.0, 1.0)
            color_val[i] = int(color_val*255)
    elif isinstance(color_val, numbers.Number):
        color_val = integer.minmax(color_val, 0.0, 1.0)
        return int(color_val * 255)

def _np_char_to_float(color_val):
    color_val = integer.minmax(color_val, 0, 255)
    return color_val/255.

_np_char_to_float = np.vectorize(_np_char_to_float, otypes=[np.float])

def char_to_float(color_val):
    if isinstance(color_val, (np.ndarray, np.generic)):
        return _np_char_to_float(color_val)
    elif isinstance(color_val, (list, tuple)):
        for i in range(len(color_val)):
            color_val[i] = integer.minmax(color_val, 0, 255)
            color_val[i] = int(color_val/255.)
    elif isinstance(color_val, numbers.Number):
        color_val = integer.minmax(color_val, 0, 255)
        return int(color_val/ 255.)

if __name__ == "__main__":
    print(float_to_char(np.array([.7,1.1,.2,.5])))
    print(char_to_float(float_to_char(np.array([.7, .35, .2, .5]))))