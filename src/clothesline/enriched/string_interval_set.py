"""
An example of interval/set kit that does not admit an underlying metric.

String form an ordered set, with e.g.
    "a" < "aa" < "aaa" < "aab" < "ab" < "b"
and infinite new strings insertable inbetween, with no well-defined 'distance',

Useful mostly as a sanity check that a metric is not assumed anywhere.

Also, rather arbitrarily (for testing purposes), string-intervals are set
to non-serializable.

Please refer to the Datetime case for relevant comments on the structure.
"""

from clothesline import IntervalSet
from clothesline.interval import Interval

from clothesline.generic.interval_generic_builder import IntervalGenericBuilder
from clothesline.generic.interval_generic_utils import IntervalGenericUtils
from clothesline.generic.interval_set_generic_utils import IntervalSetGenericUtils


class StringInterval(Interval):
    """
    Intervals between strings.
    """

    metric = None

    value_encoder = None
    value_decoder = None
    serializing_class = None
    serializing_version = None

    @staticmethod
    def builder():
        """
        The builder peg-pair -> string interval.
        """
        return IntervalGenericBuilder(
            interval_class=StringInterval,
            interval_set_class=None,
        )

    @staticmethod
    def utils():
        """
        String-interval utils
        """
        return IntervalGenericUtils(interval_class=StringInterval)


class StringIntervalSet(IntervalSet):
    """
    A string-interval-set.
    """

    interval_class = StringInterval

    metric = None

    serializing_class = None
    serializing_version = None

    @staticmethod
    def builder():
        """
        String-interval-set builder.
        """
        return IntervalGenericBuilder(
            interval_set_class=StringIntervalSet,
        )

    @staticmethod
    def utils():
        """
        Return an "utils" object configured to create special cases of
        interval sets as instance of this subclass.
        """
        return IntervalSetGenericUtils(
            interval_set_class=StringIntervalSet,
        )
