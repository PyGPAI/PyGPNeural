from idarray import IdArray
import unittest

class TestIdArray(unittest.TestCase):

    def test_add_del(self):
        arr = IdArray()
        for i in range(10):
            arr.add_id()

        for i in range(2, 5):
            arr.del_id(i)

        self.assertSequenceEqual(arr.pointers.tolist(), [0.,  1., -1., -1., -1.,  2.,  3.,  4.,  5.,  6.])
        self.assertSetEqual(arr.free_pointers, {2, 3, 4})
        self.assertEqual(arr.last_largest_id, 6)



if __name__ == '__main__':
    unittest.main()