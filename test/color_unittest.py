import color as c
import numpy as np
import unittest

class TestColor(unittest.TestCase):
    """A clamping function is usually simple enough that it shouldn't need testing, but it could be extended to different
     number types later."""
    def test_float_to_char(self):
        seq1 = [178, 255, 51, 127]
        seq2 = c.float_to_char(np.array([.7,1.1,.2,.5]))
        self.assertEqual(seq1[0], seq2[0])
        self.assertEqual(seq1[1], seq2[1])
        self.assertEqual(seq1[2], seq2[2])
        self.assertEqual(seq1[3], seq2[3])

    def test_char_to_float(self):
        seq1 = [.7,.35,.2,.5]
        seq2 = c.char_to_float(c.float_to_char(np.array([.7, .35, .2, .5])))
        self.assertAlmostEqual(seq1[0], seq2[0], delta=.02)
        self.assertAlmostEqual(seq1[1], seq2[1], delta=.02)
        self.assertAlmostEqual(seq1[2], seq2[2], delta=.02)
        self.assertAlmostEqual(seq1[3], seq2[3], delta=.02)

if __name__ == '__main__':
    unittest.main()