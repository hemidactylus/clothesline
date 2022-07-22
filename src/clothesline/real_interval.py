"""
An interval on the usual numeric domain (real numbers).
"""

from clothesline.base.base_interval import BaseInterval

#
from clothesline.generic.interval_generic_builder import IntervalGenericBuilder
from clothesline.generic.interval_generic_utils import IntervalGenericUtils
from clothesline.real_domain_metric import RealDomainMetric


class RealInterval(BaseInterval):
    """
    An interval over real numbers.
    Both a metric and serializability are defined in the following,
    in a prototypical way.

    For serializability, encoder and decoder connect a value in the domain
    (here: numbers) to something that is JSON-serializable in a deterministic
    and bijective way, i.e.
    - encoder*decoder = identity_dicts
    - decoder*encoder = identity_domain

    (infinities are treated automatically. no need to care about them.)
    Serializability metadata are provided along with the codec pair: the
    situation is the same as for RealIntervalSet (i.e. these do end up in
    the serializable dicts), so pay attention not to change them out of a whim.
    """

    metric = RealDomainMetric

    @staticmethod
    def value_encoder(val):
        """The trivial encoder."""
        return val  # noqa: PLC0116, PLC0321

    @staticmethod
    def value_decoder(val):
        """The trivial decoder."""
        return val  # noqa: PLC0116, PLC0321

    serializing_class = "RealInterval"
    serializing_version = 1

    @staticmethod
    def builder():
        """
        Create and return a "builder" for these intervals.
        Other concrete subclasses of BaseInterval need to simply
        replace `RealInterval` with whatever the class name.
        """
        return IntervalGenericBuilder(
            interval_class=RealInterval,
            interval_set_class=None,
        )

    @staticmethod
    def utils():
        """
        Create an "interval utils" object for these intervals.
        Other concrete subclasses of BaseInterval need to simply
        replace `RealInterval` with whatever the class name.
        """
        return IntervalGenericUtils(interval_class=RealInterval)
