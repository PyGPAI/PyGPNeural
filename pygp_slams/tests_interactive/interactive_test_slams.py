import unittest as ut
from .vtk_displayers import EntoColorAnimator, display_average
from svtk.vtk_displayer import VTKDisplayer
from pygp_retina.simple_average import avg_total_color
import math as m
import cv_pubsubs as cvp
class ECACallbackClass(EntoColorAnimator):
    def __init__(self):
        super(ECACallbackClass, self).__init__()
        self.i = 0
        self.ento_callback = None

    def at_start(self):
        self.add_point_field(widths=[self.red_ento.buckets, self.red_ento.num_scales*3, 1],
                             normal=[0, 1, 0],
                             center=[0, 1, 0],
                             color=[[int(128), int(66), int(21)]])
        self.update_color([0,0,0])

    def loop(self, obj, event):
        super(ECACallbackClass, self).loop(obj, event)
        self.set_all_point_colors([int(0), int(0), int(0)])
        self.set_point_colors([int(255), int(255), int(255)],
                              [self.red_indexes[i] + i * self.red_ento.buckets for i in range(len(self.red_indexes))])
        next_array_start = len(self.red_indexes)*self.red_ento.buckets
        self.set_point_colors([int(255), int(255), int(255)],
                              [next_array_start+self.green_indexes[i] + i * self.green_ento.buckets for i in range(len(self.green_indexes))])
        next_array_start += len(self.green_indexes)*self.green_ento.buckets
        self.set_point_colors([int(255), int(255), int(255)],
                              [next_array_start+self.blue_indexes[i] + i * self.blue_ento.buckets for i in range(len(self.blue_indexes))])

class TestSlams(ut.TestCase):

    def test_color(self):
        displayer = VTKDisplayer(ECACallbackClass)
        t=display_average(0, 60, True,
                          displayer.cb)
        displayer.visualize()
        cvp.webcam_pub.CamCtrl.stop_cam(0)
        t.join()


