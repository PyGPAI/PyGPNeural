import unittest as ut
import os

import numpy as np
np.set_printoptions(threshold=np.nan)

class TestGLSLCPU(ut.TestCase):
    def setUp(self):
        self.maxDiff = None

    # todo: add standalone tests
