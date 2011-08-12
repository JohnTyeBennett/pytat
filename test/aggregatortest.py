import unittest

from pytat.aggregator import Aggregator, ListAccumulator, MaxAccumulator, MinAccumulator, MeanAccumulator, object_key

class AggregatorTest(unittest.TestCase):

    def test_aggregate_list(self):
        items = [
            (1, 2, 3),
            (1, 2, 4),
            (2, 1, 3),
            (2, 1, 4),
            (1, 2, 5),
            (3, 1, 2)
        ]
        aggregated_items = Aggregator(lambda x: (x[0], x[1]), ListAccumulator).aggregate(items)
        self.assertEqual(
            [
                ((1, 2), [(1, 2, 3), (1, 2, 4), (1, 2, 5)]),
                ((2, 1), [(2, 1, 3), (2, 1, 4)]),
                ((3, 1), [(3, 1, 2)])
            ],
            aggregated_items
        )

    def test_aggregate_max(self):
        items = [
            (1, 0),
            (1, 3),
            (1, 2),
            (2, 1),
            (3, 4),
            (3, 1),
            (2, 2),
            (1, 1)
        ]
        aggregated_items = Aggregator(lambda x: x[0], MaxAccumulator).aggregate(items)
        self.assertEqual(
            [
                (1, (1, 3)),
                (2, (2, 2)),
                (3, (3, 4))
            ],
            aggregated_items
        )

    def test_aggregate_min(self):
        items = [
            (1, 0),
            (1, 3),
            (1, 2),
            (2, 1),
            (3, 4),
            (3, 1),
            (2, 2),
            (1, 1)
        ]
        aggregated_items = Aggregator(lambda x: x[0], MinAccumulator).aggregate(items)
        self.assertEqual(
            [
                (1, (1, 0)),
                (2, (2, 1)),
                (3, (3, 1))
            ],
            aggregated_items
        )

    def test_aggregate_mean(self):
        items = [
            (1, 0),
            (1, 3),
            (1, 2),
            (2, 1),
            (3, 4),
            (3, 1),
            (2, 2),
            (1, 1)
        ]
        aggregated_items = Aggregator(lambda x: x[0], MeanAccumulator, lambda x: x[1]).aggregate(items)
        self.assertEqual(
            [
                (1, 1.5),
                (2, 1.5),
                (3, 2.5)
            ],
            aggregated_items
        )

    def test_aggregate_obj(self):
        class X(object):
            def __init__(self, a, b):
                self.a = a
                self.b = b
            def __cmp__(self, other):
                return cmp((self.a, self.b), (other.a, other.b))

        items = [
            X(1, 0),
            X(1, 3),
            X(1, 2),
            X(2, 1),
            X(3, 4),
            X(3, 1),
            X(2, 2),
            X(1, 1)
        ]
        aggregated_items = Aggregator(object_key('a'), ListAccumulator).aggregate(items)
        self.assertEqual(
            [
                ((1,), [X(1, 0), X(1, 3), X(1, 2), X(1, 1)]),
                ((2,), [X(2, 1), X(2, 2)]),
                ((3,), [X(3, 4), X(3, 1)])
            ],
            aggregated_items
        )

if __name__ == '__main__':
    unittest.main()
