import unittest

from pytat.aligner import *

class AlignerTest(unittest.TestCase):

    def test_align_add(self):
        xs1 = [(1, 3), (2, 1), (4, 7), (5, 9)]
        xs2 = [(0, 1), (2, 8), (3, 6), (5, 5), (6, 4), (7, 1)]
        align_add(
            lambda x: x[0],
            xs1,
            xs2,
            lambda key: (key, 0),
        )
        self.assertEqual([(0, 0), (1, 3), (2, 1), (3, 0), (4, 7), (5, 9), (6, 0), (7, 0)], xs1)
        self.assertEqual([(0, 1), (1, 0), (2, 8), (3, 6), (4, 0), (5, 5), (6, 4), (7, 1)], xs2)

    def test_align_delete(self):
        xs1 = [(1, 3), (2, 1), (4, 7), (5, 9)]
        xs2 = [(0, 1), (2, 8), (3, 6), (5, 5), (6, 4)]
        align_delete(
            lambda x: x[0],
            xs1,
            xs2,
        )
        self.assertEqual([(2, 1), (5, 9)], xs1)
        self.assertEqual([(2, 8), (5, 5)], xs2)

if __name__ == '__main__':
    unittest.main()
