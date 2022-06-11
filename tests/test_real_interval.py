"""
Tests for the RealInterval class
"""

import unittest

from clothesline.interval_peg import IntervalPeg
from clothesline.real_interval import RealInterval
from clothesline.algebra.symbols import PlusInf, MinusInf

from clothesline.exceptions import InvalidValueError


class TestRealInterval(unittest.TestCase):
    """
    Tests for the RealInterval
    """

    @classmethod
    def setUpClass(cls):
        cls.int_utils = RealInterval.utils()
        cls.i_open = cls.int_utils.open(0.0, 1.0)
        cls.i_closed = cls.int_utils.closed(0.0, 1.0)
        cls.i_low_slice = cls.int_utils.low_slice(0.0)
        cls.i_high_slice_c = cls.int_utils.high_slice(0.0, included=True)
        cls.i_all = cls.int_utils.all()
        cls.i_int = cls.int_utils.interval(0.0, True, 1.0, False)

    def test_invalids(self):
        """ways to generate invalid intervals"""
        with self.assertRaises(InvalidValueError):
            RealInterval(
                IntervalPeg(1.0, False),
                IntervalPeg(0.0, True),
            )
        with self.assertRaises(InvalidValueError):
            RealInterval(
                IntervalPeg(0.0, False),
                IntervalPeg(0.0, True),
            )
        with self.assertRaises(InvalidValueError):
            RealInterval(
                IntervalPeg(0.0, False),
                IntervalPeg(0.0, False),
            )

    def test_creators(self):
        """ways to create intervals"""
        self.assertEqual(
            self.i_open,
            RealInterval(
                IntervalPeg(0.0, False),
                IntervalPeg(1.0, False),
            ),
        )
        self.assertEqual(
            self.i_closed,
            RealInterval(
                IntervalPeg(0.0, True),
                IntervalPeg(1.0, True),
            ),
        )
        self.assertEqual(
            self.i_low_slice,
            RealInterval(
                IntervalPeg(MinusInf, False),
                IntervalPeg(0.0, False),
            ),
        )
        self.assertEqual(
            self.i_high_slice_c,
            RealInterval(
                IntervalPeg(0.0, True),
                IntervalPeg(PlusInf, False),
            ),
        )
        self.assertEqual(
            self.i_all,
            RealInterval(
                IntervalPeg(MinusInf, False),
                IntervalPeg(PlusInf, False),
            ),
        )
        self.assertEqual(
            self.i_int,
            RealInterval(
                IntervalPeg(0.0, True),
                IntervalPeg(1.0, False),
            ),
        )

    def test_contains(self):
        """contains method"""
        i_ls_c = self.int_utils.low_slice(0.0, True)
        i_all = self.int_utils.all()
        i_int = self.int_utils.interval(0.0, False, 1.0, False)
        i_int_c = self.int_utils.interval(0.0, True, 1.0, True)
        #
        self.assertTrue(i_ls_c.contains(-1.0))
        self.assertFalse(i_ls_c.contains(1.0))
        self.assertTrue(i_ls_c.contains(0.0))
        self.assertFalse(i_ls_c.contains(MinusInf))
        #
        self.assertTrue(i_all.contains(0.0))
        self.assertFalse(i_all.contains(PlusInf))
        self.assertFalse(i_all.contains(MinusInf))
        #
        self.assertFalse(i_int.contains(MinusInf))
        self.assertFalse(i_int.contains(-1.0))
        self.assertFalse(i_int.contains(0.0))
        self.assertTrue(i_int.contains(0.5))
        self.assertFalse(i_int.contains(1.0))
        self.assertFalse(i_int.contains(2.0))
        self.assertFalse(i_int.contains(PlusInf))
        #
        self.assertFalse(i_int_c.contains(MinusInf))
        self.assertFalse(i_int_c.contains(-1.0))
        self.assertTrue(i_int_c.contains(0.0))
        self.assertTrue(i_int_c.contains(0.5))
        self.assertTrue(i_int_c.contains(1.0))
        self.assertFalse(i_int_c.contains(2.0))
        self.assertFalse(i_int_c.contains(PlusInf))

    def test_pegs(self):
        """Test the `pegs()` method"""
        peg1 = IntervalPeg(0.0, True)
        peg2 = IntervalPeg(PlusInf, False)
        itv = self.int_utils.interval(0.0, True, PlusInf, False)
        pegs_gen = itv.pegs()
        self.assertEqual(pegs_gen.__next__(), peg1)
        self.assertEqual(pegs_gen.__next__(), peg2)
        with self.assertRaises(StopIteration):
            pegs_gen.__next__()

    def test_builder(self):
        """Builder notation must give the same result as explicit creation."""
        bld = RealInterval.builder()
        self.assertEqual(
            self.i_open,
            bld(0)(1),
        )
        self.assertEqual(
            self.i_closed,
            bld[0][1],
        )
        self.assertEqual(
            self.i_low_slice,
            bld(...)(0),
        )
        self.assertEqual(
            self.i_high_slice_c,
            bld[0][...],
        )
        self.assertEqual(
            self.i_all,
            bld[...](...),
        )
        self.assertEqual(
            self.i_int,
            bld[0](1),
        )

    def test_hash(self):
        """RealInterval's hash function"""
        self.assertTrue(
            len(
                {
                    self.int_utils.open(0, 1),
                    self.int_utils.open(0, 1),
                    self.int_utils.all(),
                    self.int_utils.interval(MinusInf, False, PlusInf, False),
                }
            )
            == 2  # noqa: W503
        )


if __name__ == "__main__":
    unittest.main()
