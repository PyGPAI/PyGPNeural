import unittest as ut
from .show_v1 import show_v1

class TestDisplay(ut.TestCase):
    def test_display(self):
        t = show_v1(cam = 0,
                    request_size=(640, 480),
                    fps_limit=60)
        t.join()