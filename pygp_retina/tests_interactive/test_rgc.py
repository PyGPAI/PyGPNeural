import unittest as ut
from .show_rgc import display_rgc
from ..rgc import RGC
import os
my_dir = os.path.dirname(os.path.abspath(__file__))

# todo: find AI/Robotics competitions for test case ideas
# todo: avg time test: check single pixel changes over time, but slowly
# todo: edge test: check avg color grey, min max black and white
# todo: color test: test frequency of colors is full spectrum, avg is grey
class TestDisplay(ut.TestCase):
    def test_get_size_list(self):
        self.assertListEqual(RGC.get_size_list((1920, 1080)),
                             [[1920, 1080], [1358, 764], [960, 540], [679, 382], [480, 270], [339, 191], [240, 135],
                              [170, 95], [120, 67], [85, 47], [60, 33], [42, 23], [30, 16], [21, 11], [15, 8], [11, 6],
                              [8, 4], [6, 3], [4, 2]])

        RGC.check_size_list(RGC.get_size_list()) # assert no error raised
        RGC.get_size_list(x_scale_divisor=1) # assert no infinite loop

    def test_display(self):
        t = display_rgc(cam=0,
                        request_size=(640, 480),
                        fps_limit=60)
        t.join()

    def test_nocl_display(self):
        t = display_rgc(cam=0,
                        request_size=(640, 480),
                        fps_limit=60,
                        no_cl=True
                        )
        t.join()