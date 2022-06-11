"""
An arbitrary set defined by a finite number of intervals.
This is the base form, which has no metric imposed and assumes trivial
serializability of its values.
"""

from clothesline.base.base_interval_set import BaseIntervalSet
from clothesline.generic.interval_generic_builder import IntervalGenericBuilder
from clothesline.generic.interval_set_generic_utils import (
    IntervalSetGenericUtils,
)  # noqa: E501

#
from clothesline.real_interval import RealInterval


class RealIntervalSet(BaseIntervalSet):
    """
    A set over the real numbers, such as:
        (-inf, -5] U (-3, 3) U [4, 8)

    Interval sets over the reals are made of "RealInterval" objects,
    which is stated in the `interval_class` member.
    Also the builder() and utils() methods are defined in a standard way,
    which acts as reference for custom implementations as well.

    Note a reference to the class of "intervals making up these
    sets" is configured.

    Additionally, metadata for serializability are specified below:
    these two (class name and version) end up in the serializable dict
    to handle future 'schema changes', if there ever will be.
    """

    interval_class = RealInterval

    serializing_class = "RealIntervalSet"
    serializing_version = 1

    @staticmethod
    def builder():
        """
        Create an interval set builder.
        Other implementation need to simply replace `RealIntervalSet` here.
        """
        return IntervalGenericBuilder(
            interval_set_class=RealIntervalSet,
        )

    @staticmethod
    def utils():
        """
        Create an "utils" object, which offers standard intervalset* creation.
        Other implementation need to simply replace `RealIntervalSet` here.
        """
        return IntervalSetGenericUtils(
            interval_set_class=RealIntervalSet,
        )
