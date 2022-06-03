"""
Tests for the string-interval/set classes
"""

import unittest

from clothesline.enriched.string_interval_set import StringIntervalSet, StringInterval


class TestStringClasses(unittest.TestCase):
    """
    Tests for the string interval classes
    """

    @classmethod
    def setUpClass(cls):
        cls.ib = StringInterval.builder()
        cls.iu = StringInterval.utils()
        cls.isb = StringIntervalSet.builder()
        cls.isu = StringIntervalSet.utils()

    def test_string_interval(self):
        """StringInterval builders and utils"""
        string1 = 'some_string'
        self.assertEqual(
            self.iu.high_slice(string1),
            self.ib(string1)(...),
        )
        self.assertIs(
            type(self.iu.high_slice(string1)),
            StringInterval,
        )
        self.assertIs(
            type(self.ib(string1)(...)),
            StringInterval,
        )

    def test_string_interval_set(self):
        """StringIntervalSet builders and utils"""
        string1 = 'some_string'
        self.assertEqual(
            self.isu.high_slice(string1),
            self.isb(string1)(...),
        )
        self.assertIs(
            type(self.isu.high_slice(string1)),
            StringIntervalSet,
        )
        self.assertIs(
            type(self.isb(string1)(...)),
            StringIntervalSet,
        )

    def test_algebra(self):
        """Basic algebra using DateimeIntervalSet"""
        string0 = 'a'
        string1 = 'ab'
        string2 = 'az'
        #
        sset1 = self.isb(string0)(string1) + self.isu.high_slice(string2)
        sset2 = sset1.complement()
        sset1b = self.isb[string0][string1] + self.isu.high_slice(string2, included=True)
        sseti = sset2.intersect(sset1b)
        #
        self.assertIs(
            type(sset1),
            StringIntervalSet,
        )
        self.assertIs(
            type(sset2),
            StringIntervalSet,
        )
        self.assertEqual(
            sseti,
            self.isu.point(string0) + self.isu.point(string1) + self.isb[string2][string2]
        )

if __name__ == "__main__":
    unittest.main()
