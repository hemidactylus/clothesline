"""
Tests for the IntervalSet class
"""

import unittest

from clothesline import IntervalSet, Interval, IntervalPeg


class TestIntervalSet(unittest.TestCase):
    """
    Tests for the IntervalSet
    """

    def test_normalize(self):
        """Normalization of input intervals when creating a set"""
        is1 = IntervalSet(
            [
                Interval.open(11, 13),
                Interval.closed(10, 12),
                Interval.high_slice(15),
                Interval.interval(13, False, 14, True),
            ]
        )
        exp1 = [
            Interval.interval(10, True, 13, False),
            Interval.interval(13, False, 14, True),
            Interval.high_slice(15),
        ]
        self.assertEqual(
            is1.intervals,
            exp1,
        )

        is2 = IntervalSet(
            [
                Interval.open(10, 11),
                Interval.closed(12, 13),
                Interval.closed(8, 8),
                Interval.open(11, 12),
            ]
        )
        exp2 = [
            Interval.point(8),
            Interval.open(10, 11),
            Interval.interval(11, False, 13, True),
        ]
        self.assertEqual(
            is2.intervals,
            exp2,
        )


if __name__ == "__main__":
    unittest.main()
