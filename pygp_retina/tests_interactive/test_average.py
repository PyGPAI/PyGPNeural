import unittest as ut
from .show_average import display_average
import os
my_dir = os.path.dirname(os.path.abspath(__file__))

class TestDisplay(ut.TestCase):
    def test_display(self):
        t = display_average(cam=0,
                        request_size=(640, 480),
                        fps_limit=60)
        t.join()