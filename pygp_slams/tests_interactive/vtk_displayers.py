from pygp_ento.ento1d import EntoLine
from svtk.vtk_animation_timer_callback import VTKAnimationTimerCallback

from cv_pubsubs import webcam_pub as camp
from cv_pubsubs import window_sub as win
from pygp_retina.simple_average import avg_total_color


if False:
    from typing import Tuple

def display_average(cam,
                fps_limit=60,  # type: float
                high_speed=True,  # type: bool
                ento_animator = None
                ):
    def cam_handler(frame, cam_id):
        ento_animator.update_color(avg_total_color(frame))

    cam_thread = camp.frame_handler_thread(cam, cam_handler, fps_limit=fps_limit,
                                           high_speed=high_speed)

    return cam_thread

class EntoColorAnimator(VTKAnimationTimerCallback):
    def __init__(self):
        super(EntoColorAnimator, self).__init__()
        self.red_ento = EntoLine(255)
        self.red_ento.num_scales = 2
        self.green_ento = EntoLine(255)
        self.green_ento.num_scales = 2
        self.blue_ento = EntoLine(255)
        self.blue_ento.num_scales = 2

    def update_color(self, color):
        self.red_indexes = self.red_ento.get_indexes(color[0])
        self.green_indexes = self.green_ento.get_indexes(color[1])
        self.blue_indexes = self.blue_ento.get_indexes(color[2])

    def loop(self, obj, event):
        super(EntoColorAnimator, self).loop(obj, event)

