import unittest as ut
from .show_v1 import show_v1
from pytube import YouTube
import glob, os

class TestDisplay(ut.TestCase):
    def test_display(self):
        t = show_v1(cam = 0,
                    request_size=(640, 480),
                    fps_limit=60)
        t.join()

    def test_youtube(self):
        try:
            test_vid = glob.glob("*.webm")[0]
        except:
            yt = YouTube('https://www.youtube.com/watch?v=5IXQ6f6eMxQ', )
            yt.streams.filter(res='360p').first().download()
            test_vid = glob.glob("*.webm")[0]
        t = show_v1(cam = test_vid,
                    request_size=(640, 360),
                    fps_limit=60)
        t.join()
