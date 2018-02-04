from pygp_retina.rgc import rgc_callback
import cv2

import numpy as np
if False:
    from typing import Tuple

def col_mask_callback(
        request_size=(1280, 720),  # type: Tuple[int, int]
        relative_color_filter=True,
        edge_filter=True,
        time_filter=False,
        combine_time_and_color=False,
        gpu=None
):
        rgc_cb = rgc_callback(request_size,
                                             relative_color_filter=True,
                                             edge_filter = True,
                                             time_filter = False,
                                             combine_time_and_color = False,
                                             gpu = 1   )

        def gpu_main_update(frame  # type: np.ndarray
                            ):

            color, edge = rgc_cb(frame)

            cv2.blur(color, (3,3), dst=color)
            grey = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)

            thr = cv2.Canny(grey,50, 190)

            im2, cont, hier = cv2.findContours(thr,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for c in cont:
                perim = cv2.arcLength(c, True)
                epsilon = 0.1 *perim
                cv2.approxPolyDP(c, epsilon, True)
                bound_rect = cv2.boundingRect(c)
                x,y,w,h = bound_rect
                cv2.rectangle(color, (x, y), (x + w, y + h), (255, 0, 0))
                circ_center, circ_rad = cv2.minEnclosingCircle(c)
                cent_x, cent_y = circ_centerh
                cv2.circle(color, (int(cent_x), int(cent_y)), int(circ_rad), (255, 255, 0))
                hull = cv2.convexHull(c)
                cv2.drawContours(color, [hull], 0, (0, 255, 255))

                if len(c) > 15:
                    cv2.drawContours(color, [c], 0, (0,255,0))
                else:
                    cv2.drawContours(color, [c], 0, (0, 0, 255))

            return [color]

        return gpu_main_update


from cv_pubsubs import webcam_pub as camp
from cv_pubsubs import window_sub as win

from pygp_retina import rgc_callback

if False:
    from typing import Tuple

def display_col_mask(cam,
                    request_size=(1280, 720),  # type: Tuple[int, int]
                    fps_limit=60  # type: float
                ):
    def cam_handler(frame, cam_id):
        win.frame_dict[str(cam_id) + "Frame"] = frame

    cam_thread = camp.frame_handler_thread(cam, cam_handler, fps_limit=fps_limit,
                                           high_speed=True)

    win.sub_win_loop(names=['contour test'],

                     input_cams=[cam],
                     input_vid_global_names=[str(cam) + 'Frame'],
                     callbacks=[col_mask_callback(request_size,
                                             relative_color_filter=True,
                                             edge_filter = True,
                                             time_filter = False,
                                             combine_time_and_color = False,
                                             gpu = 1
    )])

    return cam_thread

if __name__=='__main__':
    t = display_col_mask(cam=0,
                    request_size=(640, 480),
                    fps_limit=60)

    t.join()
