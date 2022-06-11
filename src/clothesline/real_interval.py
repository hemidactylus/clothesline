"""
A single interval with a begin and and end, either open or closed at its ends.
"""

from clothesline.base.base_interval import BaseInterval
#
from clothesline.generic.interval_generic_builder import IntervalGenericBuilder
from clothesline.generic.interval_generic_utils import IntervalGenericUtils
from clothesline.real_domain_metric import RealDomainMetric


class RealInterval(BaseInterval):
    """
    A single uninterrupted interval over the universe field:
        [a,b] or (a,b) or (a,b] or [a,b)
    defined by two IntervalPeg objects. It can span to infinities.

    To allow for proper subclassing, do not mention RealInterval class
    explicitly except in the first two 'meta part' methods.
    """

    metric = RealDomainMetric

    @staticmethod
    def value_encoder(v): return v

    @staticmethod
    def value_decoder(v): return v

    serializing_class = 'RealInterval'
    serializing_version = 1

    @staticmethod
    def builder():
        """Create and return a "builder" for these intervals."""
        return IntervalGenericBuilder(
            interval_class=RealInterval,
            interval_set_class=None,
        )

    @staticmethod
    def utils():
        """Create an "interval utils" object for these intervals."""
        return IntervalGenericUtils(interval_class=RealInterval)
