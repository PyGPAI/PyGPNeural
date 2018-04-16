import unittest as ut
from .vtk_displayers import EntoLineAnimator
from svtk.vtk_displayer import VTKDisplayer

import math as m

class ELACallbackClass(EntoLineAnimator):
    def __init__(self):
        super(ELACallbackClass, self).__init__()
        self.i = 0
        self.ento_callback = None

    def at_start(self):
        self.add_point_field(widths=[64, 25, 1],
                             normal=[0, 1, 0],
                             center=[0, 1, 0],
                             color=[[int(128), int(66), int(21)]])

    def set_ento_callback(self, callback):
        self.ento_callback = callback

    def loop(self, obj, event):
        super(ELACallbackClass, self).loop(obj, event)
        indexes = self.ento_line.get_indexes(self.i)
        if self.ento_callback:
            self.i = self.ento_callback(self.i)
        self.set_all_point_colors([int(0), int(0), int(0)])
        self.set_point_colors([int(255), int(255), int(255)],
                              [indexes[i] + i * self.ento_line.buckets for i in range(len(indexes))])

class TestEnto(ut.TestCase):

    def test_iterate(self):
        displayer = VTKDisplayer(ELACallbackClass)
        displayer.cb.ento_callback = lambda x: x+1
        displayer.visualize()

    def test_poly(self):
        displayer = VTKDisplayer(ELACallbackClass)
        displayer.cb.ento_callback = lambda x: m.sqrt(x)+x+1
        displayer.visualize()