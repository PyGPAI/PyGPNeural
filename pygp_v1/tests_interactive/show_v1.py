from cv_pubsubs import webcam_pub as camp
from cv_pubsubs import window_sub as win

from pygp_v1.v1 import V1
from pygp_retina import RGC

if False:
    from typing import Tuple

def show_v1(cam,
                    request_size=(640, 480),  # type: Tuple[int, int]
                    fps_limit=60,  # type: float
                    high_speed=True,  # type: bool
                    no_cl=False  # type: bool
                ):
    def cam_handler(frame, cam_id):
        win.SubscriberWindows.frame_dict[str(cam_id) + "Frame"] = frame

    cam_thread = camp.frame_handler_thread(cam, cam_handler, fps_limit=fps_limit,
                                           high_speed=high_speed)

    v1 = V1(request_sizes=RGC.get_size_list(request_size), gpu=0, rgc=None)

    v1.is_displaying = True

    v1.setup_callback()

    callback = v1.main_callback if not no_cl else v1.nocl_callback

    win_names = ["V1 End Stop {}x{}".format(size[0], size[1]) for size in v1.request_sizes]

    win.SubscriberWindows(window_names=win_names,
                     input_cams=[cam],
                     input_vid_global_names=[str(cam) + 'Frame'],
                     callbacks=[callback]).loop()

    return cam_thread