from cv_pubsubs import webcam_pub as camp
from cv_pubsubs import window_sub as win
from pygp_retina.simple_average import avg_total_color


if False:
    from typing import Tuple

def display_average(cam,
                request_size=(1280, 720),  # type: Tuple[int, int]
                fps_limit=60,  # type: float
                high_speed=True,  # type: bool
                no_cl=False  # type: bool
                ):
    def cam_handler(frame, cam_id):
        win.SubscriberWindows.frame_dict[str(cam_id) + "Frame"] = frame

    cam_thread = camp.frame_handler_thread(cam, cam_handler, fps_limit=fps_limit,
                                           high_speed=high_speed)

    callback = avg_total_color


    win.SubscriberWindows(window_names=["avg"],
                     input_cams=[cam],
                     input_vid_global_names=[str(cam) + 'Frame'],
                     callbacks=[callback]).loop()

    return cam_thread