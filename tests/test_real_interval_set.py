"""
Tests for the RealIntervalSet class
"""

import unittest

from clothesline import RealIntervalSet
from clothesline.real_interval import RealInterval
from clothesline.algebra.symbols import PlusInf, MinusInf


class TestIntervalSet(unittest.TestCase):
    """
    Tests for the RealIntervalSet
    """

    @classmethod
    def setUpClass(cls):
        cls.is_utils = RealIntervalSet.utils()
        cls.int_utils = RealInterval.utils()
        cls.is1 = RealIntervalSet(
            [
                cls.int_utils.open(11, 13),
                cls.int_utils.closed(10, 12),
                cls.int_utils.high_slice(15),
                cls.int_utils.interval(13, False, 14, True),
            ]
        )
        cls.is2 = RealIntervalSet(
            [
                cls.int_utils.open(10, 11),
                cls.int_utils.closed(12, 13),
                cls.int_utils.closed(8, 8),
                cls.int_utils.open(11, 12),
            ]
        )
        cls.exp1_ints = [
            cls.int_utils.interval(10, True, 13, False),
            cls.int_utils.interval(13, False, 14, True),
            cls.int_utils.high_slice(15),
        ]
        cls.exp2_ints = [
            cls.int_utils.point(8),
            cls.int_utils.open(10, 11),
            cls.int_utils.interval(11, False, 13, True),
        ]
        cls.exp_u_ints = [
            cls.int_utils.point(8),
            cls.int_utils.closed(10, 14),
            cls.int_utils.high_slice(15),
        ]
        cls.isx1 = RealIntervalSet(
            [
                cls.int_utils.low_slice(-4),
                cls.int_utils.closed(-3, -1),
                cls.int_utils.interval(2, True, 3, False),
            ]
        )
        cls.isx2 = RealIntervalSet(
            [
                cls.int_utils.interval(-5, True, -2, False),
                cls.int_utils.interval(-1, False, 2, True),
                cls.int_utils.high_slice(3),
            ]
        )

    def test_equals(self):
        """Equality between interval sets."""
        int_split_closed = RealIntervalSet(
            [self.int_utils.closed(10, 11), self.int_utils.closed(11, 12)]
        )
        int_whole_closed = RealIntervalSet([self.int_utils.closed(10, 12)])
        self.assertTrue(int_split_closed == int_whole_closed)
        int_split_open = RealIntervalSet(
            [self.int_utils.open(10, 11), self.int_utils.open(11, 12)]
        )
        int_whole_open = RealIntervalSet([self.int_utils.open(10, 12)])
        self.assertFalse(int_split_open == int_whole_open)
        int_wider_open = RealIntervalSet([self.int_utils.open(10, 12.5)])
        self.assertFalse(int_whole_open == int_wider_open)
        int_split_higher = RealIntervalSet(
            [self.int_utils.closed(10, 12), self.int_utils.high_slice(11)]
        )
        int_whole_higher = RealIntervalSet(
            [self.int_utils.high_slice(10, True)]
        )  # noqa: E501
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
            list(self.is1.intervals()),
            self.exp1_ints,
        )
        self.assertEqual(
            list(self.is2.intervals()),
            self.exp2_ints,
        )

    def test_union(self):
        """Union between RealIntervalSet instances."""
        self.assertEqual(
            list((self.is1 + self.is2).intervals()),
            self.exp_u_ints,
        )
        self.assertEqual(
            list((self.is2 + self.is1).intervals()),
            self.exp_u_ints,
        )

    def test_difference(self):
        """Difference between RealIntervalSet instances."""
        self.assertEqual(
            self.is_utils.open(-2, 2) - self.is_utils.open(-1, 1),
            RealIntervalSet(
                [
                    self.int_utils.interval(-2, False, -1, True),
                    self.int_utils.interval(1, True, 2, False),
                ]
            ),
        )
        self.assertEqual(
            self.is_utils.open(5, 7)
            - RealIntervalSet(  # noqa: W503
                [
                    self.int_utils.open(5, 6),
                    self.int_utils.interval(6, True, 7, False),
                ]  # noqa: E501, PLC0301
            ),
            self.is_utils.empty(),
        )
        self.assertEqual(
            RealIntervalSet([self.int_utils.open(5, 7)])
            - RealIntervalSet([self.int_utils.open(4, 8)]),  # noqa: W503
            self.is_utils.empty(),
        )

    def test_intersection(self):
        """Intersection between RealIntervalSet instances."""
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
        x_exp = RealIntervalSet(
            [
                self.int_utils.low_slice(-5),
                self.int_utils.interval(-4, True, -3, False),
                self.int_utils.interval(-2, True, 2, False),
                self.int_utils.open(2, 3),
                self.int_utils.high_slice(3),
            ]
        )
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
        c_exp = RealIntervalSet(
            [
                self.int_utils.interval(-4, True, -3, False),
                self.int_utils.open(-1, 2),
                self.int_utils.high_slice(3, True),
            ]
        )
        self.assertEqual(
            self.isx1.complement(),
            c_exp,
        )

    def test_spurious_equality(self):
        """RealInterval is never RealIntervalSet."""
        self.assertNotEqual(
            self.int_utils.open(0, 1),
            self.is_utils.open(0, 1),
        )

    def test_hybrid_set_operations(self):
        """Set-operations allowed with an RealInterval as second operand."""
        iset = RealIntervalSet(
            [self.int_utils.open(-2, -1), self.int_utils.high_slice(1)]
        )
        self.assertEqual(
            iset + self.int_utils.closed(-1, 1),
            self.is_utils.high_slice(-2),
        )
        self.assertEqual(
            iset - self.int_utils.open(-3, 0),
            self.is_utils.high_slice(1),
        )
        self.assertEqual(
            iset.intersect(self.int_utils.interval(1, True, 3, False)),
            self.is_utils.open(1, 3),
        )
        self.assertEqual(
            iset.xor(self.int_utils.closed(-2, -1)),
            RealIntervalSet(
                [
                    self.int_utils.point(-2),
                    self.int_utils.point(-1),
                    self.int_utils.high_slice(1),
                ]
            ),
        )

    def test_superset_of(self):
        """Test of the 'superset_of' boolean test."""
        self.assertTrue(self.is1.superset_of(self.is_utils.empty()))
        self.assertTrue(
            self.is1.superset_of(
                RealIntervalSet(
                    [
                        self.int_utils.open(11, 12),
                    ]
                )
            )
        )
        self.assertTrue(
            self.is1.superset_of(
                RealIntervalSet(
                    [
                        self.int_utils.point(14),
                        self.int_utils.closed(17, 19),
                    ]
                )
            )
        )
        self.assertFalse(self.is1.superset_of(self.is_utils.point(13)))
        self.assertFalse(
            self.is1.superset_of(
                RealIntervalSet(
                    [
                        self.int_utils.open(11, 13),
                        self.int_utils.closed(13, 14),
                    ]
                )
            )
        )

    def test_builder(self):
        """Builder syntax: must yield the same as explicit creation."""
        bld = RealIntervalSet.builder()
        self.assertEqual(
            bld[10](13) + bld(13)[14] + bld(15)[...],
            self.is1,
        )
        self.assertEqual(
            bld[8][8] + bld(10)(11) + bld(11)[13],
            self.is2,
        )

    def test_hash(self):
        """RealIntervalSet's hash function"""
        self.assertTrue(
            len(
                {
                    self.is_utils.open(0, 1),
                    self.is_utils.open(0, 1),
                    self.is_utils.all(),
                    self.is_utils.interval(MinusInf, False, PlusInf, False),
                }
            )
            == 2  # noqa: W503
        )


if __name__ == "__main__":
    unittest.main()
