import unittest

from pytat.store import Store
from StringIO    import StringIO

class TestObject(object):

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __cmp__(self, other):
        return cmp((self.a, self.b, self.c), (other.a, other.b, other.c))

class TestStore(Store):

    fields = ('a', 'b', 'c')

    values_to_objects = {
        'a': int,
        'b': int,
        'c': int,
    }

    def __init__(self):
        super(TestStore, self).__init__(TestObject)

class StoreTest(unittest.TestCase):

    def test_read_store(self):
        testfile = StringIO('\n'.join((
            '{"ab": "x", "cd": "y", "ef": "z"}',
            'a,b,c',
            '1,1,1',
            '2,2,2',
            '3,3,3',
            '4,4,4',
        )))
        s = TestStore.create(testfile)
        self.assertEqual('x', s.metadata.ab)
        self.assertEqual('y', s.metadata.cd)
        self.assertEqual('z', s.metadata.ef)
        self.assertEqual(
            [
                TestObject(1, 1, 1),
                TestObject(2, 2, 2),
                TestObject(3, 3, 3),
                TestObject(4, 4, 4),
            ],
            s.entries
        )

if __name__ == '__main__':
    unittest.main()
