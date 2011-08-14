import unittest

from random      import shuffle
from pytat.stats import *

def shuffled(list):
    shuffle(list)
    return list

class StatsTest(unittest.TestCase):

    def test_mean(self):
        self.assertEqual(0.0, mean([0.0] * 10))
        self.assertEqual(0.5, mean(shuffled([float(x % 2) for x in range(10)])))
        self.assertEqual(4.5, mean(shuffled([float(x) for x in range(10)])))

    def test_median(self):
        self.assertEqual(None, median([]))
        self.assertEqual(7, median([7]))
        self.assertEqual(2, median(shuffled(range(5))))
        self.assertEqual(2.5, median(shuffled([float(x) for x in range(6)])))

    def test_stddev(self):
        self.assertEqual(0.0, stddev([]))
        self.assertEqual(0.0, stddev([4.0]))
        self.assertEqual(0.0, stddev([4.0] * 10))
        self.assertEqual(3.0276503540974917, stddev(range(10)))
        self.assertEqual(1.9771612647092462, stddev([2.5, 7.1, 3.5, 4.2]))

    def test_correlation(self):
        self.assertEqual(1.0, correlation([float(x) for x in range(10)], [float(x) for x in range(1, 11)]))
        self.assertEqual(-1.0, correlation([float(x) for x in range(10)], [float(x) for x in range(10, 0, -1)]))
        self.assertEqual(-1.0 / 7.0, correlation([1.0, 5.0, 2.0, 6.0, 4.0, 3.0], [2.0, 1.0, 4.0, 3.0, 5.0, 6.0]))

if __name__ == '__main__':
    unittest.main()
