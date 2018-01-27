import cv_pubsubs as cvp
from pygp_retina import rgc_callback

def display_rgc(cam,
                request_size=(1280, 720),  # type: Tuple[int, int]
                fps_limit=60  # type: float
                ):
    def cam_handler(frame, cam_id):
        cvp.frame_dict[str(cam_id) + "Frame"] = frame

    cam_thread = cvp.frame_handler_thread(cam, cam_handler, fps_limit=fps_limit)

    cvp.sub_win_loop(names=['RGC Relative Color Filter',
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