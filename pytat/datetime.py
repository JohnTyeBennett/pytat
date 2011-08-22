from __future__ import absolute_import

import re

from datetime  import datetime
from math      import floor

YEAR   = 'year'
MONTH  = 'month'
SECOND = 'second'
HOUR   = 'hour'
MINUTE = 'minute'
DAY    = 'day'

def pad_list(vals, num):
    newvals = [val for val in vals]
    if len(newvals) >= num:
        return newvals[0:num]
    newvals.extend([None] * max(0, num - len(newvals)))
    return newvals

class DateTime:

    __DATE_PATTERN = re.compile(r'(\d{4})-?(\d{2})-?(\d{2}) (\d{2}):(\d{2}):(\d{2})')

    __UNIT_IN_SECONDS = {
        SECOND: 1,
        MINUTE: 60,
        HOUR:   60 * 60,
        DAY:    24 * 60 * 60
    }

    __FIELD_INDEXES = {
        YEAR:   0,
        MONTH:  1,
        DAY:    2,
        HOUR:   3,
        MINUTE: 4,
        SECOND: 5,
    }

    def __init__(self, year, month, day, hour, minute, second):
        self.year   = year
        self.month  = month
        self.day    = day
        self.hour   = hour
        self.minute = minute
        self.second = second

        self.__timestamp = self.__to_timestamp()
    
    @classmethod
    def now(cls):
        now = datetime.now()
        return cls(
            now.year,
            now.month,
            now.day,
            now.hour,
            now.minute,
            now.second
        )

    @classmethod
    def from_string(cls, date_str):
        return cls.from_tuple(cls.__parse(date_str))

    @classmethod
    def from_tuple(cls, values):
        (year, month, day, hour, minute, second) = pad_list(values, 6)
        return cls(
            year   or 2000,
            month  or 1,
            day    or 1,
            hour   or 0,
            minute or 0,
            second or 0
        )

    @classmethod
    def __parse(cls, date_str):
        match = cls.__DATE_PATTERN.match(date_str)
        return (int(n) for n in match.groups())

    @classmethod
    def __from_timestamp(cls, t):
        second = t % 60
        t /= 60
        minute = t % 60
        t /= 60
        hour = t % 24
        t /= 24
        t += 0.5
        if t < 2299161:
            a = t
        else:
            x = floor((t - 1867216.25) / 36524.25)
            a = t + 1 + x - floor(x / 4)
        b = a + 1524
        c = floor((b - 122.1) / 365.25)
        d = floor(365.25 * c)
        e = floor((b - d) / 30.6001)
        day = b - d - int(30.6001 * e)
        if e < 14:
            month = e - 1
        else:
            month = e - 13
        if month > 2:
            year = c - 4716
        else:
            year = c - 4715
        return DateTime(year, month, day, hour, minute, second)

    def __to_timestamp(self):
        y = self.year
        m = self.month
        d = self.day
        if m <= 2:
            y -= 1
            m += 12
        a = int(y / 100)
        b = 2 - a + int(a / 4)
        t = int(floor(365.25 * (y + 4716)) + floor(30.6001 * (m + 1)) + d + b - 1524)
        return self.__UNIT_IN_SECONDS['day'] * t + self.__UNIT_IN_SECONDS['hour'] * self.hour + self.__UNIT_IN_SECONDS['minute'] * self.minute + self.second

    def __to_tuple(self):
        return (
            self.year,
            self.month,
            self.day,
            self.hour,
            self.minute,
            self.second
        )

    def truncate(self, unit = SECOND, num = 1):
        if unit == MONTH:
            raise Exception("Truncation to arbitrary number of months is not currently supported")
        factor = self.__UNIT_IN_SECONDS[unit] * num
        t = (self.__to_timestamp() / factor) * factor
        return self.__from_timestamp(t)

    def truncate_to(self, unit = MINUTE):
        return self.from_tuple(self.__to_tuple()[0:self.__FIELD_INDEXES[unit] + 1])

    def plus(self, num = 1, unit = SECOND):
        t = self.__timestamp + self.__UNIT_IN_SECONDS[unit] * num
        return self.__from_timestamp(t)

    def julian_day(self):
        return self.__timestamp / 24.0 / 60.0 / 60.0 - 0.5

    def __cmp__(self, other):
        if not other:
            return 1
        return cmp(self.__timestamp, other.__timestamp)

    def __str__(self):
        return '%04d-%02d-%02d %02d:%02d:%02d' % (
            self.year,
            self.month,
            self.day,
            self.hour,
            self.minute,
            self.second
        )
