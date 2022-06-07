"""
Interval and interval set subclassed to work with `datetime` values.

This serves also as prototype for other extension to specific 'real-like'
domains for subclassing and which methods should be overridden (and how).

Everything else is inherited from the superclasses in a way that takes care
of ensuring operations (utils, builders, algebraic operations)
will stay in the correct domain.
"""

import datetime

from clothesline import IntervalSet
from clothesline.interval import Interval
from clothesline.domain_metric import DomainMetric

from clothesline.generic.interval_generic_builder import IntervalGenericBuilder
from clothesline.generic.interval_generic_utils import IntervalGenericUtils
from clothesline.generic.interval_set_generic_utils import IntervalSetGenericUtils

class DatetimeMetric(DomainMetric):

    def adder(v1, v2): return v1 + v2

    def subtracter(v1, v2): return v1 - v2

    zero = datetime.timedelta(0)


class DatetimeInterval(Interval):
    """
    Domain-specific interval subclass.
    Below are the methods that one should override when creating a subclass.

    For these intervals, values are `datetime`.
    """

    metric = DatetimeMetric

    @staticmethod
    def value_encoder(v):
        return v.timestamp()

    @staticmethod
    def value_decoder(v):
        return datetime.datetime.fromtimestamp(v)

    serializing_class = 'DatetimeInterval'
    serializing_version = 1

    @staticmethod
    def builder():
        """
        Return a builder configured to make peg pairs into
        these types of intervals.
        """
        return IntervalGenericBuilder(
            interval_class=DatetimeInterval,
            interval_set_class=None,
        )

    @staticmethod
    def utils():
        """
        Return an "utils" object configured to create special cases of
        intervals as instance of this subclass.
        """
        return IntervalGenericUtils(interval_class=DatetimeInterval)


class DatetimeIntervalSet(IntervalSet):
    """
    Domain-specific interval-set subclass.
    Below are the methods that one should override when creating a subclass.

    For these interval sets, values are `datetime`.
    """

    interval_class=DatetimeInterval

    serializing_class = 'DatetimeIntervalSet'
    serializing_version = 1

    @staticmethod
    def builder():
        """
        Return a builder configured to make peg pairs into
        these types of interval sets.
        """
        return IntervalGenericBuilder(
            interval_set_class=DatetimeIntervalSet,
        )

    @staticmethod
    def utils():
        """
        Return an "utils" object configured to create special cases of
        interval sets as instance of this subclass.
        """
        return IntervalSetGenericUtils(
            interval_set_class=DatetimeIntervalSet,
        )
