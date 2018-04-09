from cv_pubsubs import webcam_pub as camp
from cv_pubsubs import window_sub as win

from pygp_v1.v1 import v1_callback, v1_nocl_callback

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
                                           high_speed=True)

    callback = v1_callback if not no_cl else v1_nocl_callback

    win.SubscriberWindows(window_names=['by','yb','bw','rg','gr', 'orient_dbg'
                            ],
                     input_cams=[cam],
                     input_vid_global_names=[str(cam) + 'Frame'],
                     callbacks=[callback(request_size,
                                             gpu = 0
    )]).loop()

    return cam_thread