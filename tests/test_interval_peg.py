"""
Tests for the IntervalPeg class
"""

import unittest

from clothesline import IntervalPeg
from clothesline.symbols import PlusInf, MinusInf
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


if __name__ == "__main__":
    unittest.main()
