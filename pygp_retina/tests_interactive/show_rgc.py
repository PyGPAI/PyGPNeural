from cv_pubsubs import webcam_pub as camp
from cv_pubsubs import window_sub as win

from pygp_retina import rgc_callback

if False:
    from typing import Tuple

def display_rgc(cam,
                request_size=(1280, 720),  # type: Tuple[int, int]
                fps_limit=60  # type: float
                ):
    def cam_handler(frame, cam_id):
        win.frame_dict[str(cam_id) + "Frame"] = frame

    cam_thread = camp.frame_handler_thread(cam, cam_handler, fps_limit=fps_limit,
                                           high_speed=True)

    win.sub_win_loop(names=['RGC Relative Color Filter',
                            'RGC Edge Filter',
                            'RGC Time Averaging Filter'
                            ],
                     input_cams=[cam],
                     input_vid_global_names=[str(cam) + 'Frame'],
                     callbacks=[rgc_callback(request_size,
                                             relative_color_filter=True,
                                             edge_filter = True,
                                             time_filter = True,
                                             combine_time_and_color = True,
                                             gpu = 1
    )])

    return cam_thread