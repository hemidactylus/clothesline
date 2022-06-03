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

    serializing_class = 'DatetimeInterval'
    serializing_version = 1

    @staticmethod
    def value_encoder(v):
        return v.timestamp()

    @staticmethod
    def builder():
        """
        Return a builder configured to make peg pairs into
        these types of intervals.
        """
        return IntervalGenericBuilder(finalizer=lambda pegs: DatetimeInterval(*pegs))

    @staticmethod
    def utils():
        """
        Return an "utils" object configured to create special cases of
        intervals as instance of this subclass.
        """
        return IntervalGenericUtils(
            int_instantiator=DatetimeInterval,
            value_decoder=lambda v: datetime.datetime.fromtimestamp(v),
            serializing_class='DatetimeInterval',
            serializing_version=1,
        )


class DatetimeIntervalSet(IntervalSet):
    """
    Domain-specific interval-set subclass.
    Below are the methods that one should override when creating a subclass.

    For these interval sets, values are `datetime`.
    """

    metric = DatetimeMetric

    serializing_class = 'DatetimeIntervalSet'
    serializing_version = 1

    @staticmethod
    def builder():
        """
        Return a builder configured to make peg pairs into
        these types of interval sets.
        """
        return IntervalGenericBuilder(finalizer = lambda pegs: DatetimeIntervalSet([DatetimeInterval(*pegs)]))

    @staticmethod
    def utils():
        """
        Return an "utils" object configured to create special cases of
        interval sets as instance of this subclass.
        """
        return IntervalSetGenericUtils(
            set_instantiator=lambda ints: DatetimeIntervalSet(ints),
            int_utils=DatetimeInterval.utils(),
            serializing_class='DatetimeIntervalSet',
            serializing_version=1,
        )

    @staticmethod
    def interval_class(*pegs):
        """
        Return the interval class this set is made of.
        """
        return DatetimeInterval
