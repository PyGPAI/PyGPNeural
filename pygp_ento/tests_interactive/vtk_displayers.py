from pygp_ento.ento1d import EntoLine
from svtk.vtk_animation_timer_callback import VTKAnimationTimerCallback

class EntoLineAnimator(VTKAnimationTimerCallback):
    def __init__(self):
        super(EntoLineAnimator, self).__init__()
        self.ento_line = EntoLine(2**32-1)

    def loop(self, obj, event):
        super(EntoLineAnimator, self).loop(obj, event)

