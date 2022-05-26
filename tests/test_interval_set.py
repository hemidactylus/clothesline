"""
Tests for the IntervalSet class
"""

import unittest

from clothesline import IntervalSet
from clothesline.interval_peg import IntervalPeg
from clothesline.interval import Interval
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
        cls.is_utils = IntervalSet.utils()

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
            self.is_utils.open(-2, 2) - self.is_utils.open(-1, 1),
            IntervalSet(
                [
                    Interval.interval(-2, False, -1, True),
                    Interval.interval(1, True, 2, False),
                ]
            ),
        )
        self.assertEqual(
            self.is_utils.open(5, 7)
            - IntervalSet([Interval.open(5, 6), Interval.interval(6, True, 7, False)]),
            self.is_utils.empty(),
        )
        self.assertEqual(
            IntervalSet([Interval.open(5, 7)]) - IntervalSet([Interval.open(4, 8)]),
            self.is_utils.empty(),
        )

    def test_intersection(self):
        """Intersection between IntervalSet instances."""
        self.assertEqual(
            self.is_utils.open(0, 2).intersect(self.is_utils.open(1, 3)),
            self.is_utils.open(1, 2),
        )
        self.assertEqual(
            self.is_utils.closed(0, 1).intersect(self.is_utils.closed(2, 3)),
            self.is_utils.empty(),
        )
        self.assertEqual(
            self.is_utils.all().intersect(self.is1),
            self.is1,
        )
        self.assertEqual(
            self.is_utils.all().intersect(self.is2),
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

    def test_spurious_equality(self):
        """Interval is never IntervalSet."""
        self.assertNotEqual(
            Interval.open(0, 1),
            self.is_utils.open(0, 1),
        )

    def test_hybrid_set_operations(self):
        """Set-operations allowed with an Interval as second operand."""
        iset = IntervalSet([Interval.open(-2, -1), Interval.high_slice(1)])
        self.assertEqual(
            iset + Interval.closed(-1, 1),
            self.is_utils.high_slice(-2),
        )
        self.assertEqual(
            iset - Interval.open(-3, 0),
            self.is_utils.high_slice(1),
        )
        self.assertEqual(
            iset.intersect(Interval.interval(1, True, 3, False)),
            self.is_utils.open(1, 3),
        )
        self.assertEqual(
            iset.xor(Interval.closed(-2, -1)),
            IntervalSet([
                Interval.point(-2),
                Interval.point(-1),
                Interval.high_slice(1),
            ]),
        )

    def test_superset_of(self):
        """Test of the 'superset_of' boolean test."""
        self.assertTrue(self.is1.superset_of(self.is_utils.empty()))
        self.assertTrue(self.is1.superset_of(IntervalSet([
            Interval.open(11, 12),
        ])))
        self.assertTrue(self.is1.superset_of(IntervalSet([
            Interval.point(14),
            Interval.closed(17, 19),
        ])))
        self.assertFalse(self.is1.superset_of(self.is_utils.point(13)))
        self.assertFalse(self.is1.superset_of(IntervalSet([
            Interval.open(11, 13),
            Interval.closed(13, 14),
        ])))

    def test_builder(self):
        """Builder syntax: must yield the same as explicit creation."""
        b = IntervalSet.builder()
        self.assertEqual(
            b[10](13) + b(13)[14] + b(15)[...],
            self.is1,
        )
        self.assertEqual(
            b[8][8] + b(10)(11) + b(11)[13],
            self.is2,
        )

    def test_hash(self):
        """IntervalSet's hash function"""
        self.assertTrue(
            len(
                {
                    self.is_utils.open(0, 1),
                    self.is_utils.open(0, 1),
                    self.is_utils.all(),
                    self.is_utils.interval(MinusInf, False, PlusInf, False),
                }
            )
            == 2
        )

if __name__ == "__main__":
    unittest.main()
