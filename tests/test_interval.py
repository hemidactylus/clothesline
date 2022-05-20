"""
Tests for the Interval class
"""

import unittest

from clothesline import Interval, IntervalPeg
from clothesline.symbols import PlusInf, MinusInf

from clothesline.exceptions import InvalidValueError


class TestInterval(unittest.TestCase):
    """
    Tests for the Interval
    """

    def test_invalids(self):
        """ways to generate invalid intervals"""
        with self.assertRaises(InvalidValueError):
            Interval(
                IntervalPeg(1.0, False),
                IntervalPeg(0.0, True),
            )
        with self.assertRaises(InvalidValueError):
            Interval(
                IntervalPeg(0.0, False),
                IntervalPeg(0.0, True),
            )
        with self.assertRaises(InvalidValueError):
            Interval(
                IntervalPeg(0.0, False),
                IntervalPeg(0.0, False),
            )

    def test_creators(self):
        """ways to create intervals"""
        i_open = Interval.open(0.0, 1.0)
        i_closed = Interval.closed(0.0, 1.0)
        i_low_slice = Interval.low_slice(0.0)
        i_high_slice_c = Interval.high_slice(0.0, included=True)
        i_all = Interval.all()
        i_int = Interval.interval(0.0, True, 1.0, False)
        self.assertEqual(
            i_open,
            Interval(
                IntervalPeg(0.0, False),
                IntervalPeg(1.0, False),
            ),
        )
        self.assertEqual(
            i_closed,
            Interval(
                IntervalPeg(0.0, True),
                IntervalPeg(1.0, True),
            ),
        )
        self.assertEqual(
            i_low_slice,
            Interval(
                IntervalPeg(MinusInf, False),
                IntervalPeg(0.0, False),
            ),
        )
        self.assertEqual(
            i_high_slice_c,
            Interval(
                IntervalPeg(0.0, True),
                IntervalPeg(PlusInf, False),
            ),
        )
        self.assertEqual(
            i_all,
            Interval(
                IntervalPeg(MinusInf, False),
                IntervalPeg(PlusInf, False),
            ),
        )
        self.assertEqual(
            i_int,
            Interval(
                IntervalPeg(0.0, True),
                IntervalPeg(1.0, False),
            ),
        )

    def test_contains(self):
        """contains method"""
        i_ls_c = Interval.low_slice(0.0, True)
        i_all = Interval.all()
        i_int = Interval.interval(0.0, False, 1.0, False)
        i_int_c = Interval.interval(0.0, True, 1.0, True)
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
        itv = Interval.interval(0.0, True, PlusInf, False)
        pegsGen = itv.pegs()
        self.assertEqual(pegsGen.__next__(), peg1)
        self.assertEqual(pegsGen.__next__(), peg2)
        with self.assertRaises(StopIteration):
            pegsGen.__next__()


if __name__ == "__main__":
    unittest.main()
