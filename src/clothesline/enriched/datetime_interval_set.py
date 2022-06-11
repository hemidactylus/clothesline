"""
Interval and interval set subclassed to work with `datetime` values.

This serves also as prototype for other extension to specific 'real-like'
domains for subclassing and which methods should be overridden (and how).

Everything else is inherited from the superclasses in a way that takes care
of ensuring operations (utils, builders, algebraic operations)
will stay in the correct domain.
"""

import datetime

from clothesline.base.base_interval_set import BaseIntervalSet
from clothesline.base.base_interval import BaseInterval
from clothesline.base.base_domain_metric import BaseDomainMetric

from clothesline.generic.interval_generic_builder import IntervalGenericBuilder
from clothesline.generic.interval_generic_utils import IntervalGenericUtils
from clothesline.generic.interval_set_generic_utils import (
    IntervalSetGenericUtils,
)  # noqa: E501


class DatetimeMetric(BaseDomainMetric):
    """
    The metric on the datetime domain just needs to take care
    of the fact that differences are 'timedelta' objects.
    """

    @staticmethod
    def adder(val1, val2):
        """standard addition."""
        return val1 + val2

    @staticmethod
    def subtracter(val1, val2):
        """standard subtraction."""
        return val1 - val2

    zero = datetime.timedelta(0)


class DatetimeInterval(BaseInterval):
    """
    Domain-specific interval subclass.
    Below are the methods that one should override when creating a subclass.

    For these intervals, values are `datetime`.
    """

    metric = DatetimeMetric

    @staticmethod
    def value_encoder(val):
        """domain encoder: datetime => timestamp (floating-point number)."""
        return val.timestamp()

    @staticmethod
    def value_decoder(val):
        """domain decoder: timestamp -> datetime."""
        return datetime.datetime.fromtimestamp(val)

    serializing_class = "DatetimeInterval"
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


class DatetimeIntervalSet(BaseIntervalSet):
    """
    Domain-specific interval-set subclass.
    Below are the methods that one should override when creating a subclass.

    For these interval sets, values are `datetime`.
    """

    interval_class = DatetimeInterval

    serializing_class = "DatetimeIntervalSet"
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
