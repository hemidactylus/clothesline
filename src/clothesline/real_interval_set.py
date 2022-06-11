"""
An arbitrary set defined by a finite number of intervals.
This is the base form, which has no metric imposed and assumes trivial
serializability of its values.
"""

from clothesline.base.base_interval_set import BaseIntervalSet
from clothesline.generic.interval_generic_builder import IntervalGenericBuilder
from clothesline.generic.interval_set_generic_utils import IntervalSetGenericUtils
#
from clothesline.real_interval import RealInterval


class RealIntervalSet(BaseIntervalSet):
    """
    A portion of the continuous line (e.g. the reals + infinities)
    defined by an arbitrary (finite) number of RealInterval objects.

    References to `RealIntervalSet` itself are to be limited and controlled,
    so that a superclass (e.g. providing special metric/serialization etc) has
    no trouble.

    Richer classes with metric/serializability requirements have to
    subclass this one and just redefine builder(), utils() and a few properties
    which are the only places where explicit class references
    (for instantiation) can be used.
    """

    ## "Meta part", i.e. items to override when subclassing.

    interval_class = RealInterval

    serializing_class = 'RealIntervalSet'
    serializing_version = 1

    @staticmethod
    def builder():
        """
        Create an interval set builder.
        """
        return IntervalGenericBuilder(
            interval_set_class=RealIntervalSet,
        )

    @staticmethod
    def utils():
        """
        Create an "utils" object, offering standard intervalset* creation.
        """
        return IntervalSetGenericUtils(
            interval_set_class=RealIntervalSet,
        )
