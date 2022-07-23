"""
Any set over the domain, defined by a finite number of intervals.
"""

from functools import reduce

from clothesline.algebra import combine_intervals
from clothesline.algebra.symbols import x_sum

#
from clothesline.exceptions import MetricNotImplementedError


class BaseIntervalSet:
    """
    Any portion of the "continuous line" that is the domain
    (such as the reals + infinities), defined by an arbitrary (finite) number
    of intervals.

    Any concrete implementation has to provide: a `builder()` and a `utils()`
    (in a pretty standard way, see e.g. the reference "real*" implementation),
    as well as to give the name of the class representing the individual
    intervals this set is made of.
    Moreover, serializing signature data can be provided (if so desired and if
    serializability is supported by the underlying interval implementation).
    """

    interval_class = None

    serializing_class = None
    serializing_version = None

    @staticmethod
    def builder():
        """
        Create an interval set builder.
        """

    @staticmethod
    def utils():
        """
        Create an "utils" object, offering standard intervalset* creation.
        """

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
            "class": self.serializing_class,
            "version": self.serializing_version,
            "intervals": [interval.to_dict() for interval in self._intervals],
        }

    def contains(self, value):
        """
        Test whether a value belongs to the set.

        Conventionally, infinities do not belong to any interval set.
        """
        return any(interval.contains(value) for interval in self._intervals)

    def extension(self):
        """
        If a metric is defined for this interval type,
        use it to compute this interval set's (overall) 'extension'.
        """
        if self.interval_class.metric:  # noqa: PLR1705

            def c_sum(val1, val2):
                return x_sum(
                    val1,
                    val2,
                    self.interval_class.metric.adder,
                )

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
            and len(self._intervals) == len(other._intervals)  # noqa: W503
            and self._intervals == other._intervals  # noqa: W503
        )

    def __hash__(self):
        return hash(
            (
                self.__class__,
                tuple((hash(interval) for interval in self._intervals)),
            )  # noqa: E501
        )

    def __repr__(self):
        if not self._intervals:  # noqa: PLR1705
            return "{}"
        else:
            return " U ".join(
                interval.__repr__() for interval in self._intervals
            )  # noqa: E501

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
