from pygp_retina.rgc import rgc_callback
import cv2

import numpy as np
if False:
    from typing import Tuple, List, Any
import math

# check every pixel for equilateral/right
def col_mask_callback(
        request_size=(1280, 720),  # type: Tuple[int, int]
        draw_keypoints=True,
        gpu=1
):
        rgc_cb = rgc_callback(request_size,
                              relative_color_filter=False,
                                             gpu = gpu   )

        kp_store = ([],[])
        orb = cv2.ORB_create()

        FLANN_INDEX_LSH = 6
        index_params = dict(algorithm=FLANN_INDEX_LSH, trees=5)
        search_params = dict(checks=50)  # or pass empty dictionary
        flann = cv2.FlannBasedMatcher(index_params, search_params)

        edge_original = []

        def gpu_main_update(frame  # type: np.ndarray
                            ):
            nonlocal kp_store, orb, flann, edge_original

            edges = rgc_cb(frame)
            edge = edges[0]

            kp = orb.detect(edge, None) # type: List[Any]
            kp, des = orb.compute(edge, kp)

            if len(kp_store[0]) <=0:
                kp_store = (kp, des)


            matches = flann.knnMatch(des, kp_store[1], k=2)

            # Need to draw only good matches, so create a mask
            matchesMask = [[0, 0] for _ in range(len(matches))]

            edge = cv2.cvtColor(edge,cv2.COLOR_GRAY2BGR)


            for m in range(len(matches)):
                if len(matches[m]) != 2:
                    continue
                a, b = matches[m]
                if a.distance < 0.8 * b.distance:
                    if draw_keypoints:
                        pt1 = (int(kp[m].pt[0]), int(kp[m].pt[1]))
                        pt2 = (int(kp[m].pt[0]+math.cos(math.radians(kp[m].angle))*kp[m].size),
                               int(kp[m].pt[1]+math.sin(math.radians(kp[m].angle))*kp[m].size))
                        match_amount = min(((b.distance - a.distance)/float(b.distance))*3.0, 1.0)
                        edge = cv2.arrowedLine(edge, pt1, pt2, (int(kp[m].response*255),int((match_amount)*255),int((1-match_amount)*255)), 1)
                    matchesMask[m] = [1, 0]

            draw_params = dict(matchColor=(0, 255, 255),
                               singlePointColor=(0, 0, 255),
                               matchesMask=matchesMask,
                               flags=0)

            if len(edge_original) == 0:
                edge_original = edge


            if draw_keypoints:
                edge = cv2.drawMatchesKnn(edge, kp, edge_original, kp_store[0], matches, None, **draw_params)
            edges[0] = edge

            return (edges[0],)

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
                                           high_speed=False)

    win.sub_win_loop(names=['by_np','yb_np','bw_np','rg_np','gr_np'],

                     input_cams=[cam],
                     input_vid_global_names=[str(cam) + 'Frame'],
                     callbacks=[col_mask_callback(request_size,
                                             gpu = 1
    )])

    return cam_thread

if __name__=='__main__':
    t = display_col_mask(cam=0,
                    request_size=(1280, 720),
                    fps_limit=60)

    t.join()
