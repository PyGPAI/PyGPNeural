import unittest as ut
from cv_pubsubs import window_sub as win
from cv_pubsubs import webcam_pub as cam

import os
my_dir = os.path.dirname(os.path.abspath(__file__))

class TestSubWin(ut.TestCase):

    def test_sub(self):
        def cam_handler(frame, cam_id):
            win.frame_dict[str(cam_id) + "Frame"] = (frame, frame)

        cam_id = 0

        t = cam.frame_handler_thread(cam_id=cam_id,
                                     frame_handler=cam_handler,
                                   request_size=(480, 336),
                                   high_speed=False,
                                   fps_limit=24
                                   )

        win.sub_win_loop(names=['cammy'],
                     input_vid_global_names=[str(cam_id) + "Frame"])

        cam.CamCtrl.stop_cam(cam_id)

        t.join()
