import unittest

from pytat.datetime import *

class DateTimeTest(unittest.TestCase):

    def test_from_string(self):
        for s, (year, month, day, hour, minute, second, julian_day) in (
            ('2000-01-01 12:00:00', (2000, 1,  1, 12, 0, 0, 2451545.0)),
            ('1999-01-01 00:00:00', (1999, 1,  1,  0, 0, 0, 2451179.5)),
            ('1987-01-27 00:00:00', (1987, 1, 27,  0, 0, 0, 2446822.5)),
            ('1987-06-19 12:00:00', (1987, 6, 19, 12, 0, 0, 2446966.0)),
            ('1988-01-27 00:00:00', (1988, 1, 27,  0, 0, 0, 2447187.5)),
            ('1900-01-01 00:00:00', (1900, 1,  1,  0, 0, 0, 2415020.5)),
            ('1600-01-01 00:00:00', (1600, 1,  1,  0, 0, 0, 2305447.5)),
        ):
            dt = DateTime.from_string(s)
            self.assertEqual(year,       dt.year)
            self.assertEqual(month,      dt.month)
            self.assertEqual(day,        dt.day)
            self.assertEqual(hour,       dt.hour)
            self.assertEqual(minute,     dt.minute)
            self.assertEqual(second,     dt.second)
            self.assertEqual(julian_day, dt.julian_day())

    def test_plus(self):
        self.assertEqual(DateTime.from_string('2011-08-27 12:34:00'), DateTime.from_string('2011-08-20 12:34:00').plus( 7, DAY))
        self.assertEqual(DateTime.from_string('2011-08-19 12:34:00'), DateTime.from_string('2011-08-20 12:34:00').plus(-1, DAY))
        self.assertEqual(DateTime.from_string('2011-01-02 12:34:00'), DateTime.from_string('2010-12-30 12:34:00').plus( 3, DAY))
        self.assertEqual(DateTime.from_string('2011-01-02 12:35:05'), DateTime.from_string('2011-01-02 12:34:00').plus(65))

    def test_truncate_to(self):
        dt = DateTime.from_string('2011-08-20 12:34:56')
        self.assertEqual(DateTime.from_string('2011-08-20 12:34:00'), dt.truncate_to(MINUTE))
        self.assertEqual(DateTime.from_string('2011-08-20 12:00:00'), dt.truncate_to(HOUR))
        self.assertEqual(DateTime.from_string('2011-08-20 00:00:00'), dt.truncate_to(DAY))
        self.assertEqual(DateTime.from_string('2011-08-01 00:00:00'), dt.truncate_to(MONTH))
        self.assertEqual(DateTime.from_string('2011-01-01 00:00:00'), dt.truncate_to(YEAR))

    def test_truncate(self):
        self.assertEqual(DateTime.from_string('2011-08-20 12:00:00'), DateTime.from_string('2011-08-20 12:02:00').truncate(MINUTE, 15))
        self.assertEqual(DateTime.from_string('2011-08-20 12:00:00'), DateTime.from_string('2011-08-20 12:07:00').truncate(MINUTE, 15))
        self.assertEqual(DateTime.from_string('2011-08-20 12:15:00'), DateTime.from_string('2011-08-20 12:15:00').truncate(MINUTE, 15))
        self.assertEqual(DateTime.from_string('2011-08-20 12:15:00'), DateTime.from_string('2011-08-20 12:29:00').truncate(MINUTE, 15))
        self.assertEqual(DateTime.from_string('2011-07-31 00:00:00'), DateTime.from_string('2011-07-31 12:29:00').truncate(DAY, 2))
        self.assertEqual(DateTime.from_string('2011-07-31 00:00:00'), DateTime.from_string('2011-08-01 12:29:00').truncate(DAY, 2))
        self.assertEqual(DateTime.from_string('2011-08-20 00:00:00'), DateTime.from_string('2011-08-20 12:29:00').truncate(DAY, 2))
        self.assertEqual(DateTime.from_string('2011-08-20 00:00:00'), DateTime.from_string('2011-08-21 12:29:00').truncate(DAY, 2))
        self.assertEqual(DateTime.from_string('2011-08-22 00:00:00'), DateTime.from_string('2011-08-22 12:29:00').truncate(DAY, 2))
        self.assertEqual(DateTime.from_string('2011-08-22 00:00:00'), DateTime.from_string('2011-08-23 12:29:00').truncate(DAY, 2))

if __name__ == '__main__':
    unittest.main()
