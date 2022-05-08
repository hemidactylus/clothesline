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

    def test_peg_ordering(self):  # noqa: PLR0915
        """Inequalities between pegs"""
        p_a = IntervalPeg(MinusInf, False)
        p_a2 = IntervalPeg(MinusInf, False)
        p_0 = IntervalPeg(-1.0, True)
        p_1 = IntervalPeg(-1.0, False)
        p_2 = IntervalPeg(1.0, True)
        p_2b = IntervalPeg(1.0, True)
        p_3 = IntervalPeg(1.0, False)
        p_z = IntervalPeg(PlusInf, False)

        # equalities
        self.assertEqual(p_a, p_a2)
        self.assertEqual(p_2, p_2b)

        # lesser-than
        self.assertLess(p_a, p_0)
        self.assertLess(p_a, p_1)
        self.assertLess(p_a, p_2)
        self.assertLess(p_a, p_3)
        self.assertLess(p_a, p_z)
        #
        self.assertLess(p_0, p_1)
        self.assertLess(p_0, p_2)
        self.assertLess(p_0, p_3)
        self.assertLess(p_0, p_z)
        #
        self.assertLess(p_1, p_2)
        self.assertLess(p_1, p_3)
        self.assertLess(p_1, p_z)
        #
        self.assertLess(p_2, p_3)
        self.assertLess(p_2, p_z)
        #
        self.assertLess(p_3, p_z)

        # greater-than
        self.assertGreater(p_0, p_a)
        self.assertGreater(p_1, p_a)
        self.assertGreater(p_2, p_a)
        self.assertGreater(p_3, p_a)
        self.assertGreater(p_z, p_a)
        #
        self.assertGreater(p_1, p_0)
        self.assertGreater(p_2, p_0)
        self.assertGreater(p_3, p_0)
        self.assertGreater(p_z, p_0)
        #
        self.assertGreater(p_2, p_1)
        self.assertGreater(p_3, p_1)
        self.assertGreater(p_z, p_1)
        #
        self.assertGreater(p_3, p_2)
        self.assertGreater(p_z, p_2)
        #
        self.assertGreater(p_z, p_3)

        # lesser-or-equal-than
        self.assertLessEqual(p_a, p_a)
        self.assertLessEqual(p_a, p_0)
        self.assertLessEqual(p_a, p_1)
        self.assertLessEqual(p_a, p_2)
        self.assertLessEqual(p_a, p_3)
        self.assertLessEqual(p_a, p_z)
        #
        self.assertLessEqual(p_0, p_0)
        self.assertLessEqual(p_0, p_1)
        self.assertLessEqual(p_0, p_2)
        self.assertLessEqual(p_0, p_3)
        self.assertLessEqual(p_0, p_z)
        #
        self.assertLessEqual(p_1, p_1)
        self.assertLessEqual(p_1, p_2)
        self.assertLessEqual(p_1, p_3)
        self.assertLessEqual(p_1, p_z)
        #
        self.assertLessEqual(p_2, p_2)
        self.assertLessEqual(p_2, p_3)
        self.assertLessEqual(p_2, p_z)
        #
        self.assertLessEqual(p_3, p_3)
        self.assertLessEqual(p_3, p_z)
        #
        self.assertLessEqual(p_z, p_z)

        # greater-or-equal-than
        self.assertGreaterEqual(p_a, p_a)
        self.assertGreaterEqual(p_0, p_a)
        self.assertGreaterEqual(p_1, p_a)
        self.assertGreaterEqual(p_2, p_a)
        self.assertGreaterEqual(p_3, p_a)
        self.assertGreaterEqual(p_z, p_a)
        #
        self.assertGreaterEqual(p_0, p_0)
        self.assertGreaterEqual(p_1, p_0)
        self.assertGreaterEqual(p_2, p_0)
        self.assertGreaterEqual(p_3, p_0)
        self.assertGreaterEqual(p_z, p_0)
        #
        self.assertGreaterEqual(p_1, p_1)
        self.assertGreaterEqual(p_2, p_1)
        self.assertGreaterEqual(p_3, p_1)
        self.assertGreaterEqual(p_z, p_1)
        #
        self.assertGreaterEqual(p_2, p_2)
        self.assertGreaterEqual(p_3, p_2)
        self.assertGreaterEqual(p_z, p_2)
        #
        self.assertGreaterEqual(p_3, p_3)
        self.assertGreaterEqual(p_z, p_3)
        #
        self.assertGreaterEqual(p_z, p_z)


if __name__ == "__main__":
    unittest.main()
