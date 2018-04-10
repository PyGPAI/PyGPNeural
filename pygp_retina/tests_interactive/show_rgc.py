from cv_pubsubs import webcam_pub as camp
from cv_pubsubs import window_sub as win

from pygp_retina import RGC


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

    rgc = RGC(request_sizes=RGC.get_size_list(request_size),
              relative_color_filter=True,
              edge_filter=False,
              time_filter=False,
              combine_time_and_color=False,
              gpu=0)

    rgc.displaying = True

    rgc.setup_callback()

    callback = rgc.main_callback if not no_cl else rgc.rgc_nocl_callback

    win_names = ['RGC Scaled Output {}x{}'.format(size[0], size[1]) for size in rgc.request_sizes]
    win_names.extend(['RGC Color Edge Filter {}x{}'.format(size[0], size[1]) for size in rgc.request_sizes])
    #win_names.extend(['RGC Edge Filter {}x{}'.format(size[0], size[1]) for size in rgc.request_sizes])

    win.SubscriberWindows(window_names=win_names,
                     input_cams=[cam],
                     input_vid_global_names=[str(cam) + 'Frame'],
                     callbacks=[callback]).loop()

    return cam_thread