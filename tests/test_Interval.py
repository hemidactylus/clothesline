import unittest

from clothesline import Interval, IntervalPeg
from clothesline.symbols import PLUS_INF, MINUS_INF

from clothesline.exceptions import InvalidValueError

class TestInterval(unittest.TestCase):

    def test_invalids(self):
        with self.assertRaises(InvalidValueError):
            i1 = Interval(
                IntervalPeg(0.0, True),
                IntervalPeg(PLUS_INF, True),
            )
        with self.assertRaises(InvalidValueError):
            i2 = Interval(
                IntervalPeg(MINUS_INF, True),
                IntervalPeg(0.0, False),
            )
        with self.assertRaises(InvalidValueError):
            i3 = Interval(
                IntervalPeg(1.0, False),
                IntervalPeg(0.0, True),
            )

    def test_creators(self):
        i_open = Interval.Open(0.0, 1.0)
        i_closed = Interval.Closed(0.0, 1.0)
        i_lowSlice = Interval.LowSlice(0.0)
        i_highSliceC = Interval.HighSlice(0.0, included=True)
        i_all = Interval.All()
        i_int = Interval.Interval(0.0, True, 1.0, False)
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
            i_lowSlice,
            Interval(
                IntervalPeg(MINUS_INF, False),
                IntervalPeg(0.0, False),
            ),
        )
        self.assertEqual(
            i_highSliceC,
            Interval(
                IntervalPeg(0.0, True),
                IntervalPeg(PLUS_INF, False),
            ),
        )
        self.assertEqual(
            i_all,
            Interval(
                IntervalPeg(MINUS_INF, False),
                IntervalPeg(PLUS_INF, False),
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
        i_lsC = Interval.LowSlice(0.0, True)
        i_all = Interval.All()
        i_int = Interval.Interval(0.0, False, 1.0, False)
        i_intC = Interval.Interval(0.0, True, 1.0, True)
        #
        self.assertTrue(i_lsC.contains(-1.0))
        self.assertFalse(i_lsC.contains(1.0))
        self.assertTrue(i_lsC.contains(0.0))
        self.assertTrue(i_lsC.contains(MINUS_INF))
        #
        self.assertTrue(i_all.contains(0.0))
        self.assertTrue(i_all.contains(PLUS_INF))
        self.assertTrue(i_all.contains(MINUS_INF))
        #
        self.assertFalse(i_int.contains(MINUS_INF))
        self.assertFalse(i_int.contains(-1.0))
        self.assertFalse(i_int.contains(0.0))
        self.assertTrue(i_int.contains(0.5))
        self.assertFalse(i_int.contains(1.0))
        self.assertFalse(i_int.contains(2.0))
        self.assertFalse(i_int.contains(PLUS_INF))
        #
        self.assertFalse(i_intC.contains(MINUS_INF))
        self.assertFalse(i_intC.contains(-1.0))
        self.assertTrue(i_intC.contains(0.0))
        self.assertTrue(i_intC.contains(0.5))
        self.assertTrue(i_intC.contains(1.0))
        self.assertFalse(i_intC.contains(2.0))
        self.assertFalse(i_intC.contains(PLUS_INF))

if __name__ == '__main__':
    unittest.main()
