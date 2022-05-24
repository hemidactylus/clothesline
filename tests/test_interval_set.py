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
        cls.isx1 = IntervalSet([
            Interval.low_slice(-4),
            Interval.closed(-3, -1),
            Interval.interval(2, True, 3, False),
        ])
        cls.isx2 = IntervalSet([
            Interval.interval(-5, True, -2, False),
            Interval.interval(-1, False, 2, True),
            Interval.high_slice(3),
        ])

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

    def test_normalize(self):
        """Normalization of input intervals when creating a set"""
        self.assertEqual(
            self.is1._intervals,
            self.exp1_ints,
        )
        self.assertEqual(
            self.is2._intervals,
            self.exp2_ints,
        )

    def test_union(self):
        """Union between IntervalSet instances."""
        self.assertEqual(
            (self.is1 + self.is2)._intervals,
            self.exp_u_ints,
        )
        self.assertEqual(
            (self.is2 + self.is1)._intervals,
            self.exp_u_ints,
        )

    def test_difference(self):
        """Difference between IntervalSet instances."""
        self.assertEqual(
            IntervalSet.open(-2, 2) - IntervalSet.open(-1, 1),
            IntervalSet(
                [
                    Interval.interval(-2, False, -1, True),
                    Interval.interval(1, True, 2, False),
                ]
            ),
        )
        self.assertEqual(
            IntervalSet.open(5, 7)
            - IntervalSet([Interval.open(5, 6), Interval.interval(6, True, 7, False)]),
            IntervalSet.empty(),
        )
        self.assertEqual(
            IntervalSet([Interval.open(5, 7)]) - IntervalSet([Interval.open(4, 8)]),
            IntervalSet.empty(),
        )

    def test_intersection(self):
        """Intersection between IntervalSet instances."""
        self.assertEqual(
            IntervalSet.open(0, 2).intersect(IntervalSet.open(1, 3)),
            IntervalSet.open(1, 2),
        )
        self.assertEqual(
            IntervalSet.closed(0, 1).intersect(IntervalSet.closed(2, 3)),
            IntervalSet.empty(),
        )
        self.assertEqual(
            IntervalSet.all().intersect(self.is1),
            self.is1,
        )
        self.assertEqual(
            IntervalSet.all().intersect(self.is2),
            self.is2,
        )

    def test_xor(self):
        """XOR between interval sets."""
        x_exp = IntervalSet([
            Interval.low_slice(-5),
            Interval.interval(-4, True, -3, False),
            Interval.interval(-2, True, 2, False),
            Interval.open(2, 3),
            Interval.high_slice(3),
        ])
        self.assertEqual(
            self.isx1.xor(self.isx2),
            x_exp,
        )
        self.assertEqual(
            self.isx2.xor(self.isx1),
            x_exp,
        )

    def test_complement(self):
        """Complement of an interval set."""
        c_exp = IntervalSet([
            Interval.interval(-4, True, -3, False),
            Interval.open(-1, 2),
            Interval.high_slice(3, True),
        ])
        self.assertEqual(
            self.isx1.complement(),
            c_exp,
        )

if __name__ == "__main__":
    unittest.main()
