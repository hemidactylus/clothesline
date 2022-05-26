"""
Tests for the IntervalPeg class
"""

import unittest

from clothesline.interval_peg import IntervalPeg
from clothesline.algebra.symbols import PlusInf, MinusInf
from clothesline.exceptions import InvalidValueError


class TestIntervalPeg(unittest.TestCase):
    """
    Tests for the IntervalPeg
    """

    def test_faulty_pegs(self):
        """Ways to create invalid pegs"""
        with self.assertRaises(InvalidValueError):
            IntervalPeg(PlusInf, True)
        with self.assertRaises(InvalidValueError):
            IntervalPeg(MinusInf, True)

    def test_hashable_pegs(self):
        """Hashability and equality tests"""
        self.assertTrue(IntervalPeg(0.0, True) == IntervalPeg(0.0, True))
        self.assertTrue(IntervalPeg(PlusInf, False) == IntervalPeg(PlusInf, False))
        self.assertFalse(IntervalPeg(PlusInf, False) == IntervalPeg(0.0, True))
        self.assertFalse(IntervalPeg(0.0, False) == IntervalPeg(0.0, True))
        self.assertFalse(IntervalPeg(0.0, False) == IntervalPeg(1.0, False))
        #
        self.assertTrue(
            len(
                {
                    IntervalPeg(1.0 + 1.0, True),
                    IntervalPeg(2.0, True),
                    IntervalPeg(PlusInf, False),
                    IntervalPeg(PlusInf, not True),
                }
            )
            == 2
        )


if __name__ == "__main__":
    unittest.main()
