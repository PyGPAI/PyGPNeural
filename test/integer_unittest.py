import integer as b
import unittest

class TestClamp(unittest.TestCase):
    """A clamping function is usually simple enough that it shouldn't need testing, but it could be extended to different
     number types later."""
    def test_above(self):
        self.assertEqual(b.minmax(100,0,20),20)

    def test_below(self):
        self.assertEqual(b.minmax(-100,0,20),0)

    def test_in(self):
        self.assertEqual(b.minmax(10,0,20),10)

    def test_fail(self):
        self.assertRaises(AssertionError, b.minmax, 5, -2, -7)

    def test_nth_middle(self):
        self.assertEqual(b.nth_middle(0, 0, 10), 5)
        self.assertEqual(b.nth_middle(1, 0, 10), 2.5)
        self.assertEqual(b.nth_middle(2, 0, 10), 7.5)

if __name__ == '__main__':
    unittest.main()
