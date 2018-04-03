import unittest as ut
from .show_v1 import show_v1
from pytube import YouTube
import glob, os

class TestDisplay(ut.TestCase):
    def test_display(self):
        t = show_v1(cam = 0,
                    request_size=(640,480),
                    fps_limit=60)
        t.join()

    def test_nocl_display(self):
        t = show_v1(cam = 0,
                    request_size=(640,480),
                    fps_limit=60,
                    no_cl=True)
        t.join()

    def test_youtube(self):
        # end stop: 8 pixels immediate surrounding. inhibit+excite immediate neighbors.
        # If too much, inhibit/excite semidistant neighbors.
        t = show_v1(cam = self.test_vid,
                    request_size=(1280, 720),
                    fps_limit=60)
        t.join()
