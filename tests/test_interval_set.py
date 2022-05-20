"""
Tests for the IntervalSet class
"""

import unittest

from clothesline import IntervalSet, Interval, IntervalPeg
from clothesline.symbols import PlusInf, MinusInf


class TestIntervalSet(unittest.TestCase):
    """
    Tests for the IntervalSet
    """

    @classmethod
    def setUpClass(cls):
        cls.is1 = IntervalSet(
            [
                Interval.open(11, 13),
                Interval.closed(10, 12),
                Interval.high_slice(15),
                Interval.interval(13, False, 14, True),
            ]
        )
        cls.is2 = IntervalSet(
            [
                Interval.open(10, 11),
                Interval.closed(12, 13),
                Interval.closed(8, 8),
                Interval.open(11, 12),
            ]
        )
        cls.exp1_ints = [
            Interval.interval(10, True, 13, False),
            Interval.interval(13, False, 14, True),
            Interval.high_slice(15),
        ]
        cls.exp2_ints = [
            Interval.point(8),
            Interval.open(10, 11),
            Interval.interval(11, False, 13, True),
        ]
        cls.exp_u_ints = [
            Interval.point(8),
            Interval.closed(10, 14),
            Interval.high_slice(15),
        ]

    def test_normalize(self):
        """Normalization of input intervals when creating a set"""
        self.assertEqual(
            self.is1.intervals,
            self.exp1_ints,
        )
        self.assertEqual(
            self.is2.intervals,
            self.exp2_ints,
        )

    def test_union(self):
        """Union between IntervalSet instances."""
        self.assertEqual(
            (self.is1 + self.is2).intervals,
            self.exp_u_ints,
        )
        self.assertEqual(
            (self.is2 + self.is1).intervals,
            self.exp_u_ints,
        )

    def test_equals(self):
        """Equality between interval sets."""
        int_split_closed = IntervalSet(
            [Interval.closed(10, 11), Interval.closed(11, 12)]
        )
        int_whole_closed = IntervalSet([Interval.closed(10, 12)])
        self.assertTrue(int_split_closed == int_whole_closed)
        int_split_open = IntervalSet([Interval.open(10, 11), Interval.open(11, 12)])
        int_whole_open = IntervalSet([Interval.open(10, 12)])
        self.assertFalse(int_split_open == int_whole_open)
        int_wider_open = IntervalSet([Interval.open(10, 12.5)])
        self.assertFalse(int_whole_open == int_wider_open)
        int_split_higher = IntervalSet(
            [Interval.closed(10, 12), Interval.high_slice(11)]
        )
        int_whole_higher = IntervalSet([Interval.high_slice(10, True)])
        self.assertTrue(int_split_higher == int_whole_higher)

    def test_contains(self):
        """Test of values belonging to interval sets."""
        self.assertFalse(self.is1.contains(9))
        self.assertTrue(self.is1.contains(10))
        self.assertTrue(self.is1.contains(11))
        self.assertFalse(self.is1.contains(13))
        self.assertTrue(self.is1.contains(14))
        self.assertFalse(self.is1.contains(14.5))
        self.assertFalse(self.is1.contains(15))
        self.assertTrue(self.is1.contains(20))
        self.assertFalse(self.is1.contains(PlusInf))


if __name__ == "__main__":
    unittest.main()
