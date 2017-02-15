import numpy_helpers as h
import numpy as np
import unittest

class TestNormalize(unittest.TestCase):
    def test_3d(self):
        axis = np.array([1,2,3])
        normalized = h.normalize(axis)
        self.assertAlmostEqual(normalized[0][0], 0.26726124)
        self.assertAlmostEqual(normalized[0][1], 0.53452248)
        self.assertAlmostEqual(normalized[0][2], 0.80178373)

if __name__ == '__main__':
    unittest.main()
