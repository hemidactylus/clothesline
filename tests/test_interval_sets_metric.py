"""
Tests for the metric enrichment for interval sets*
"""

import unittest
from datetime import datetime, timedelta

from clothesline import IntervalSet
from clothesline import DatetimeIntervalSet
from clothesline.algebra.symbols import PlusInf, MinusInf
from clothesline.enriched.string_interval_set import StringIntervalSet, StringInterval

from clothesline.exceptions import MetricNotImplementedError


class TestIntervalSetMetric(unittest.TestCase):
    """
    Tests for the metric of IntervalSet.
    """

    @classmethod
    def setUpClass(cls):
        cls.utils = IntervalSet.utils()
        cls.builder = IntervalSet.builder()

    def test_interval_lengths(self):
        """IntervalSet's extension() method."""
        is1 = self.builder[0](2)            \
            + self.builder(1)[5]            \
            + self.utils.open(100, 150)     \
            + self.utils.closed(1000, 1500)
        self.assertEqual(
            is1.extension(),
            555,
        )
        self.assertEqual(
            self.builder(0)[...].extension(),
            PlusInf,
        )

class TestDatetimeIntervalSetMetric(unittest.TestCase):
    """
    Tests for the metric of DatetimeIntervalSet.
    """

    @classmethod
    def setUpClass(cls):
        cls.utils = DatetimeIntervalSet.utils()
        cls.builder = DatetimeIntervalSet.builder()

    def test_interval_lengths(self):
        """DatetimeIntervalSet's extension() method."""
        dt0 =    datetime(2000, 10, 20, 12, 34, 56)
        dt1 =    dt0 + timedelta(days=1)
        dt2 =    dt0 + timedelta(days=2)
        dt5 =    dt0 + timedelta(days=5)
        dt100 =  dt0 + timedelta(days=100)
        dt150 =  dt0 + timedelta(days=150)
        dt1000 = dt0 + timedelta(days=1000)
        dt1500 = dt0 + timedelta(days=1500)
        #
        is1 = self.builder[dt0](dt2)            \
            + self.builder(dt1)[dt5]            \
            + self.utils.open(dt100, dt150)     \
            + self.utils.closed(dt1000, dt1500)
        self.assertEqual(
            is1.extension(),
            timedelta(days=555),
        )
        self.assertEqual(
            self.builder(dt0)[...].extension(),
            PlusInf,
        )

class TestStringIntervalSetMetric(unittest.TestCase):
    """
    Test for the (not defined) metric of StringInterval/Set
    """

    def test_interval_lengths(self):
        with self.assertRaises(MetricNotImplementedError):
            StringInterval.builder()['a']('z').extension()

    def test_interval_set_lengths(self):
        with self.assertRaises(MetricNotImplementedError):
            StringIntervalSet.builder()['a']('z').extension()

if __name__ == "__main__":
    unittest.main()
