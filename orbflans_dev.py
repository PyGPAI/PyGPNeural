from pygp_retina.rgc import RGC
import cv2
import pickle as pickle
import numpy as np
if False:
    from typing import Tuple, List, Any
import math

#https://isotope11.com/blog/storing-surf-sift-orb-keypoints-using-opencv-in-python
def pickle_keypoints(keypoints, descriptors):
    i = 0
    temp_array = []
    for point in keypoints:
        temp = (point.pt, point.size, point.angle, point.response, point.octave,
        point.class_id, descriptors[i])
        i+=1
        temp_array.append(temp)
    return temp_array

def unpickle_keypoints(array):
    keypoints = []
    descriptors = []
    for point in array:
        temp_feature = cv2.KeyPoint(x=point[0][0],y=point[0][1],_size=point[1], _angle=point[2], _response=point[3], _octave=point[4], _class_id=point[5])
        temp_descriptor = point[6]
        keypoints.append(temp_feature)
        descriptors.append(temp_descriptor)
    return keypoints, np.array(descriptors)

import pubsub, threading
from cv_pubsubs import listen_default
def print_keys_thread():
    sub_key = pubsub.subscribe("CVKeyStroke")
    sub_cmd = pubsub.subscribe("CVWinCmd")
    msg_cmd = ''
    while msg_cmd != 'quit':
        key_chr = listen_default(sub_key, timeout=.1)  # type: np.ndarray
        if key_chr is not None:
            print("key pressed: " + str(key_chr))
        msg_cmd = listen_default(sub_cmd, block=False, empty='')
    pubsub.publish("CVWinCmd", 'quit')


def start_print_keys_thread():  # type: (...) -> threading.Thread
    t = threading.Thread(target=print_keys_thread, args=())
    t.start()
    return t

# check every pixel for equilateral/right
def col_mask_callback(
        request_size=(1280, 720),  # type: Tuple[int, int]
        draw_keypoints=True,
        gpu=1
):
    rgc = RGC( [request_size], relative_color_filter=False )

    rgc.setup_callback()
    rgc.displaying = True

    rgc_cb = rgc.main_callback

    kp_store = ([],[])
    orb = cv2.ORB_create()

    FLANN_INDEX_LSH = 6
    index_params = dict(algorithm=FLANN_INDEX_LSH, trees=5)
    search_params = dict(checks=50)  # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    edge_original = []

    i=0
    def gpu_main_update(frame  # type: np.ndarray
                        ):
        nonlocal kp_store, orb, flann, edge_original, i, rgc

        i+=1
        rgc_cb(frame)
        edge = rgc.current_bundle.scaled_edges[0]

        kp = orb.detect(edge, None) # type: List[Any]
        kp, des = orb.compute(edge, kp)

        if len(kp_store[0]) <=0:
            kp_store = (kp, des)

        temp = pickle_keypoints(kp, des)
        pickle.dump(temp, open("keypoints_database{}.p".format(i), "wb"))

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

        return (edge,)

    return gpu_main_update


from cv_pubsubs import webcam_pub as camp
from cv_pubsubs import window_sub as win


if False:
    from typing import Tuple

def display_col_mask(cam,
                    request_size=(1280, 720),  # type: Tuple[int, int]
                    fps_limit=60  # type: float
                ):
    def cam_handler(frame, cam_id):
        win.SubscriberWindows.frame_dict[str(cam_id) + "Frame"] = frame

    cam_thread = camp.frame_handler_thread(cam, cam_handler, fps_limit=fps_limit,
                                           high_speed=False)

    win.SubscriberWindows(window_names=['by_np','yb_np','bw_np','rg_np','gr_np'],

                     input_cams=[cam],
                     input_vid_global_names=[str(cam) + 'Frame'],
                     callbacks=[col_mask_callback(request_size,
                                             gpu = 1
    )]).loop()

    return cam_thread

if __name__=='__main__':
    t = display_col_mask(cam=0,
                    request_size=(1280, 720),
                    fps_limit=60)

    t.join()
