import unittest

from pytat.aligner import *

class AlignerTest(unittest.TestCase):

    def test_align_add(self):
        xs = [(1, 3), (2, 1), (4, 7), (5, 9)]
        ys = [(0, 1), (2, 8), (3, 6), (5, 5), (6, 4), (7, 1)]
        zs = []
        ws = [(5, 1)]
        align_add(
            lambda x: x[0],
            lambda key: (key, 0),
            xs,
            ys,
            zs,
            ws
        )
        self.assertEqual([(0, 0), (1, 3), (2, 1), (3, 0), (4, 7), (5, 9), (6, 0), (7, 0)], xs)
        self.assertEqual([(0, 1), (1, 0), (2, 8), (3, 6), (4, 0), (5, 5), (6, 4), (7, 1)], ys)
        self.assertEqual([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)], zs)
        self.assertEqual([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 1), (6, 0), (7, 0)], ws)

    def test_align_delete(self):
        xs = [(1, 3), (2, 1), (4, 7), (5, 9)]
        ys = [(0, 1), (2, 8), (3, 6), (5, 5), (6, 4)]
        zs = [(0, 4), (2, 6), (5, 2)]
        align_delete(lambda x: x[0], xs, ys, zs)
        self.assertEqual([(2, 1), (5, 9)], xs)
        self.assertEqual([(2, 8), (5, 5)], ys)
        self.assertEqual([(2, 6), (5, 2)], zs)

if __name__ == '__main__':
    unittest.main()
