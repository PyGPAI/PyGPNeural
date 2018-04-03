import unittest as ut
from .show_rgc import display_rgc

import os
my_dir = os.path.dirname(os.path.abspath(__file__))

# todo: find AI/Robotics competitions for test case ideas
# todo: avg time test: check single pixel changes over time, but slowly
# todo: edge test: check avg color grey, min max black and white
# todo: color test: test frequency of colors is full spectrum, avg is grey
class TestDisplay(ut.TestCase):
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