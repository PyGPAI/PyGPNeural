from cv_pubsubs import webcam_pub as camp
from cv_pubsubs import window_sub as win

from pygp_retina import rgc_callback, rgc_nocl_callback


if False:
    from typing import Tuple

def display_rgc(cam,
                request_size=(1280, 720),  # type: Tuple[int, int]
                fps_limit=60,  # type: float
                high_speed=True,  # type: bool
                no_cl=False  # type: bool
                ):
    def cam_handler(frame, cam_id):
        win.SubscriberWindows.frame_dict[str(cam_id) + "Frame"] = frame

    cam_thread = camp.frame_handler_thread(cam, cam_handler, fps_limit=fps_limit,
                                           high_speed=high_speed)

    callback = rgc_callback if not no_cl else rgc_nocl_callback

    win.SubscriberWindows(window_names=['RGC Relative Color Filter',
                            'RGC Edge Filter',
                            'RGC Time Averaging Filter'
                            ],
                     input_cams=[cam],
                     input_vid_global_names=[str(cam) + 'Frame'],
                     callbacks=[callback(request_size,
                                             relative_color_filter=True,
                                             edge_filter = True,
                                             gpu = 0)

                                ]).loop()

    return cam_thread