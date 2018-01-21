import cv_pubsubs as cvp
from pygp_retina import rgc_callback

def display_rgc(cam,
                request_size=(1280, 720),  # type: Tuple[int, int]
                fps_limit=60  # type: float
                ):
    def cam_handler(frame, cam_id):
        cvp.frameDict[str(cam_id) + "Frame"] = frame

    cam_thread = cvp.frame_handler_thread(cam, cam_handler, fps_limit=fps_limit)

    cvp.sub_win_loop(names=['RGC Relative Color Filter',
                            'RGC Edge Filter',
                            'RGC Time Averaging Filter'],
                     input_cams=[cam],
                     input_vid_global_names=[str(cam) + 'Frame'],
                     callbacks=[rgc_callback(request_size)])

    return cam_thread