from cv_pubsubs import webcam_pub as camp
from cv_pubsubs import window_sub as win

from pygp_v1.v1 import v1_callback

if False:
    from typing import Tuple

def show_v1(cam,
                    request_size=(1280, 720),  # type: Tuple[int, int]
                    fps_limit=60  # type: float
                ):
    def cam_handler(frame, cam_id):
        win.frame_dict[str(cam_id) + "Frame"] = frame

    cam_thread = camp.frame_handler_thread(cam, cam_handler, fps_limit=fps_limit,
                                           high_speed=True)

    win.sub_win_loop(names=['orient_dbg_np'
                            ],
                     input_cams=[cam],
                     input_vid_global_names=[str(cam) + 'Frame'],
                     callbacks=[v1_callback(request_size,
                                             gpu = 0
    )])

    return cam_thread