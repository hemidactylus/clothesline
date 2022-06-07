"""
An arbitrary set defined by a finite number of intervals.
This is the base form, which has no metric imposed and assumes trivial
serializability of its values.
"""

from functools import reduce

from clothesline.interval import Interval
from clothesline.algebra import combine_intervals
from clothesline.algebra.symbols import x_sum
#
from clothesline.generic.interval_generic_builder import IntervalGenericBuilder
from clothesline.generic.interval_set_generic_utils import IntervalSetGenericUtils
from clothesline.domain_metric import DomainMetric
#
from clothesline.exceptions import MetricNotImplementedError


class IntervalSet:
    """
    A portion of the continuous line (e.g. the reals + infinities)
    defined by an arbitrary (finite) number of Interval objects.

    References to `IntervalSet` itself are to be limited and controlled,
    so that a superclass (e.g. providing special metric/serialization etc) has
    no trouble.

    Richer classes with metric/serializability requirements have to
    subclass this one and just redefine builder(), utils() and a few properties
    which are the only places where explicit class references
    (for instantiation) can be used.
    """

    ## "Meta part", i.e. items to override when subclassing.

    interval_class = Interval

    serializing_class = 'IntervalSet'
    serializing_version = 1

    @staticmethod
    def builder():
        """
        Create an interval set builder.
        """
        return IntervalGenericBuilder(
            interval_set_class=IntervalSet,
        )

    @staticmethod
    def utils():
        """
        Create an "utils" object, offering standard intervalset* creation.
        """
        return IntervalSetGenericUtils(
            interval_set_class=IntervalSet,
        )

    ## "Regular methods" follow (which use instantiations from the meta part).

    def __init__(self, intervals):
        self._intervals = self._normalize(intervals)

    def _normalize(self, intervals):
        """
        An arbitrary input of intervals (overlapping, unsorted)
        is reduced to 'normal form' using the one-single-list
        form of the generic combiner.
        """
        return combine_intervals(self.interval_class, [intervals])

    def to_dict(self):
        """
        Return a json-encodable representation of this interval set.
        """
        return {
            'class': self.serializing_class,
            'version': self.serializing_version,
            'intervals': [
                interval.to_dict()
                for interval in self._intervals
            ]
        }

    def contains(self, value):
        """
        Test whether a value belongs to the set.

        Conventionally, infinities do not belong to any interval set.
        """
        return any(interval.contains(value) for interval in self._intervals)

    def extension(self):
        if self.interval_class.metric:
            def c_sum(v1, v2): return x_sum(v1, v2, self.interval_class.metric.adder)
            return reduce(
                c_sum,
                (interval.extension() for interval in self._intervals),
                self.interval_class.metric.zero,
            )
        else:
            raise MetricNotImplementedError
 
    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and len(self._intervals) == len(other._intervals)
            and self._intervals == other._intervals
        )

    def __hash__(self):
        return hash((
            self.__class__,
            tuple((
                hash(interval)
                for interval in self._intervals
            ))
        ))

    def __repr__(self):
        if self._intervals == []:
            return "{}"
        else:
            return " U ".join(interval.__repr__() for interval in self._intervals)

    def __add__(self, other):
        """Alias for set-wise union."""
        return self.union(other)

    def __sub__(self, other):
        """Alias for set-wise difference."""
        return self.difference(other)

    def intervals(self):
        """Return an iterable over the intervals of this set."""
        for interval in self._intervals:
            yield interval

    def union(self, other):
        """
        Union of interval sets.
        """
        return self.__class__(
            combine_intervals(
                self.interval_class,
                [self._intervals, other.intervals()],
                combiner_function=lambda q: q[0] or q[1],
            )
        )

    def difference(self, other):
        """
        Difference of interval sets.
        """
        return self.__class__(
            combine_intervals(
                self.interval_class,
                [self._intervals, other.intervals()],
                combiner_function=lambda q: q[0] and not q[1],
            )
        )

    def intersect(self, other):
        """
        Intersection of interval sets.
        """
        return self.__class__(
            combine_intervals(
                self.interval_class,
                [self._intervals, other.intervals()],
                combiner_function=lambda q: q[0] and q[1],
            )
        )

    def xor(self, other):
        """
        XOR ("exclusive disjunction") of interval sets.
        """
        return self.__class__(
            combine_intervals(
                self.interval_class,
                [self._intervals, other.intervals()],
                combiner_function=lambda q: q[0] ^ q[1],
            )
        )

    def complement(self):
        """
        Set complement of the interval set.
        """
        return self.utils().all().difference(self)

    def superset_of(self, other):
        """Test whether another interval(set) is contained in this."""
        return other - self == self.utils().empty()
