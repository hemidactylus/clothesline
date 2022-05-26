"""
An arbitrary set defined by a finite number of intervals.
This is the base form, which has no metric imposed and assumes trivial
serializability of its values.
"""

from clothesline.interval import Interval
from clothesline.algebra import combine_intervals
#
from clothesline.interval_generic_builder import IntervalGenericBuilder
from clothesline.interval_set_generic_utils import IntervalSetGenericUtils

class IntervalSet:
    """
    A portion of the continuous line (e.g. the reals + infinities)
    defined by an arbitrary (finite) number of Interval objects.

    References to `IntervalSet` itself are to be limited and controlled,
    so that a superclass (e.g. providing metric/serialization etc) has
    no trouble.

    IntervalSet is the "minimal" interval set class:
        - no metric is assumed
        - no special needs for serializability are allowed.

    Richer classes with metric/serializability requirements have to
    subclass this one and just redefine builder() and utils(),
    which are the only method where explicit class references
    (for instantiation) can be used.
    """

    ## "Meta part", i.e. method to override when subclassing.

    @staticmethod
    def builder():
        """
        Create an interval set builder.
        """
        return IntervalGenericBuilder(finalizer = lambda pegs: IntervalSet([Interval(*pegs)]))

    @staticmethod
    def utils():
        """
        Create an "utils" object, offering standard intervalset* creation.
        """
        return IntervalSetGenericUtils(
            set_instantiator=lambda ints: IntervalSet(ints),
            int_utils=Interval.utils(),
        )

    ## "Regular methods" follow (which use instantiations from the meta part).

    def __init__(self, intervals):
        """`intervals` is a list of Interval instances."""
        self._intervals = self._normalize(intervals)

    @staticmethod
    def _normalize(intervals):
        """
        An arbitrary input of intervals (overlapping, unsorted)
        is reduced to 'normal form' using the one-single-list
        form of the generic combiner.
        """
        return combine_intervals([intervals])

    def contains(self, value):
        """
        Test whether a value belongs to the set.

        Conventionally, infinities do not belong to any interval set.
        """
        return any(interval.contains(value) for interval in self._intervals)

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
