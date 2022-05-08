import unittest

from clothesline import IntervalPeg
from clothesline.symbols import PLUS_INF, MINUS_INF
from clothesline.exceptions import InvalidValueError

class TestIntervalPeg(unittest.TestCase):

    def test_faultyPegs(self):
        with self.assertRaises(InvalidValueError):
            p1 = IntervalPeg(PLUS_INF, True)
        with self.assertRaises(InvalidValueError):
            p2 = IntervalPeg(MINUS_INF, True)

    def test_pegOrdering(self):
        pA = IntervalPeg(MINUS_INF, False)
        pA2 = IntervalPeg(MINUS_INF, False)
        p0 = IntervalPeg(-1.0, True)
        p1 = IntervalPeg(-1.0, False)
        p2 = IntervalPeg(1.0, True)
        p2b = IntervalPeg(1.0, True)
        p3 = IntervalPeg(1.0, False)
        pZ = IntervalPeg(PLUS_INF, False)

        # equalities
        self.assertEqual(pA, pA2)
        self.assertEqual(p2, p2b)

        # lesser-than
        self.assertLess(pA, p0)
        self.assertLess(pA, p1)
        self.assertLess(pA, p2)
        self.assertLess(pA, p3)
        self.assertLess(pA, pZ)
        #
        self.assertLess(p0, p1)
        self.assertLess(p0, p2)
        self.assertLess(p0, p3)
        self.assertLess(p0, pZ)
        #
        self.assertLess(p1, p2)
        self.assertLess(p1, p3)
        self.assertLess(p1, pZ)
        #
        self.assertLess(p2, p3)
        self.assertLess(p2, pZ)
        #
        self.assertLess(p3, pZ)

        # greater-than
        self.assertGreater(p0, pA)
        self.assertGreater(p1, pA)
        self.assertGreater(p2, pA)
        self.assertGreater(p3, pA)
        self.assertGreater(pZ, pA)
        #
        self.assertGreater(p1, p0)
        self.assertGreater(p2, p0)
        self.assertGreater(p3, p0)
        self.assertGreater(pZ, p0)
        #
        self.assertGreater(p2, p1)
        self.assertGreater(p3, p1)
        self.assertGreater(pZ, p1)
        #
        self.assertGreater(p3, p2)
        self.assertGreater(pZ, p2)
        #
        self.assertGreater(pZ, p3)

        # lesser-or-equal-than
        self.assertLessEqual(pA, pA)
        self.assertLessEqual(pA, p0)
        self.assertLessEqual(pA, p1)
        self.assertLessEqual(pA, p2)
        self.assertLessEqual(pA, p3)
        self.assertLessEqual(pA, pZ)
        #
        self.assertLessEqual(p0, p0)
        self.assertLessEqual(p0, p1)
        self.assertLessEqual(p0, p2)
        self.assertLessEqual(p0, p3)
        self.assertLessEqual(p0, pZ)
        #
        self.assertLessEqual(p1, p1)
        self.assertLessEqual(p1, p2)
        self.assertLessEqual(p1, p3)
        self.assertLessEqual(p1, pZ)
        #
        self.assertLessEqual(p2, p2)
        self.assertLessEqual(p2, p3)
        self.assertLessEqual(p2, pZ)
        #
        self.assertLessEqual(p3, p3)
        self.assertLessEqual(p3, pZ)
        #
        self.assertLessEqual(pZ, pZ)

        # greater-or-equal-than
        self.assertGreaterEqual(pA, pA)
        self.assertGreaterEqual(p0, pA)
        self.assertGreaterEqual(p1, pA)
        self.assertGreaterEqual(p2, pA)
        self.assertGreaterEqual(p3, pA)
        self.assertGreaterEqual(pZ, pA)
        #
        self.assertGreaterEqual(p0, p0)
        self.assertGreaterEqual(p1, p0)
        self.assertGreaterEqual(p2, p0)
        self.assertGreaterEqual(p3, p0)
        self.assertGreaterEqual(pZ, p0)
        #
        self.assertGreaterEqual(p1, p1)
        self.assertGreaterEqual(p2, p1)
        self.assertGreaterEqual(p3, p1)
        self.assertGreaterEqual(pZ, p1)
        #
        self.assertGreaterEqual(p2, p2)
        self.assertGreaterEqual(p3, p2)
        self.assertGreaterEqual(pZ, p2)
        #
        self.assertGreaterEqual(p3, p3)
        self.assertGreaterEqual(pZ, p3)
        #
        self.assertGreaterEqual(pZ, pZ)


if __name__ == '__main__':
    unittest.main()
