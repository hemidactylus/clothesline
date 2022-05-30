"""
Tests for the datetime-enriched classes
"""

import unittest
from datetime import datetime

from clothesline import DatetimeIntervalSet
from clothesline.enriched.datetime_interval_set import DatetimeInterval


class TestDatetimeClasses(unittest.TestCase):
    """
    Tests for the enriched DatetimeIntervalSet / DatetimeInterval
    """

    @classmethod
    def setUpClass(cls):
        cls.ib = DatetimeInterval.builder()
        cls.iu = DatetimeInterval.utils()
        cls.isb = DatetimeIntervalSet.builder()
        cls.isu = DatetimeIntervalSet.utils()

    def test_datetime_interval(self):
        """DatetimeInterval builders and utils"""
        date1 = datetime(2010, 1, 1)
        self.assertEqual(
            self.iu.high_slice(date1),
            self.ib(date1)(...),
        )
        self.assertIs(
            type(self.iu.high_slice(date1)),
            DatetimeInterval,
        )
        self.assertIs(
            type(self.ib(date1)(...)),
            DatetimeInterval,
        )

    def test_datetime_interval_set(self):
        """DatetimeIntervalSet builders and utils"""
        date1 = datetime(2010, 1, 1)
        self.assertEqual(
            self.isu.high_slice(date1),
            self.isb(date1)(...),
        )
        self.assertIs(
            type(self.isu.high_slice(date1)),
            DatetimeIntervalSet,
        )
        self.assertIs(
            type(self.isb(date1)(...)),
            DatetimeIntervalSet,
        )

    def test_algebra(self):
        """Basic algebra using DateimeIntervalSet"""
        date0 = datetime(2010, 1, 1)
        date1 = datetime(2011, 1, 1)
        date2 = datetime(2012, 1, 1)
        #
        dset1 = self.isb(date0)(date1) + self.isu.high_slice(date2)
        dset2 = dset1.complement()
        dset1b = self.isb[date0][date1] + self.isu.high_slice(date2, included=True)
        dseti = dset2.intersect(dset1b)
        #
        self.assertIs(
            type(dset1),
            DatetimeIntervalSet,
        )
        self.assertIs(
            type(dset2),
            DatetimeIntervalSet,
        )
        self.assertEqual(
            dseti,
            self.isu.point(date0) + self.isu.point(date1) + self.isb[date2][date2]
        )
