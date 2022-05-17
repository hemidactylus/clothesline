"""
Tests for the IntervalSet class
"""

import unittest

from clothesline import IntervalSet, Interval, IntervalPeg
# from clothesline.symbols import PlusInf, MinusInf

# from clothesline.exceptions import InvalidValueError


class TestIntervalSet(unittest.TestCase):
    """
    Tests for the IntervalSet
    """

    def test_normalize(self):
        """Normalization of input intervals when creating a set"""
        is1 = IntervalSet([
            Interval.open(11,13),
            Interval.closed(10,12),
            Interval.high_slice(15),
            Interval.interval(13, False, 14, True),
        ])
        print(is1)

if __name__ == "__main__":
    unittest.main()
