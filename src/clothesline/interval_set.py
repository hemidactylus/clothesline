"""
An arbitrary set defined by a finite number of intervals.
"""

from clothesline import Interval
from clothesline.algebra import combine_intervals


class IntervalSet:
    """
    A portion of the continuous line (e.g. the reals + infinities)
    defined by an arbitrary (finite) number of Interval objects.
    """

    _intervals = None

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
            isinstance(other, IntervalSet)
            and len(self._intervals) == len(other._intervals)
            and self._intervals == other._intervals
        )

    def __hash__(self):
        return hash(tuple((
            hash(interval)
            for interval in self._intervals
        )))

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
        return IntervalSet(
            combine_intervals(
                [self._intervals, other.intervals()],
                combiner_function=lambda q: q[0] or q[1],
            )
        )

    def difference(self, other):
        """
        Difference of interval sets.
        """
        return IntervalSet(
            combine_intervals(
                [self._intervals, other.intervals()],
                combiner_function=lambda q: q[0] and not q[1],
            )
        )

    def intersect(self, other):
        """
        Intersection of interval sets.
        """
        return IntervalSet(
            combine_intervals(
                [self._intervals, other.intervals()],
                combiner_function=lambda q: q[0] and q[1],
            )
        )

    def xor(self, other):
        """
        XOR ("exclusive disjunction") of interval sets.
        """
        return IntervalSet(
            combine_intervals(
                [self._intervals, other.intervals()],
                combiner_function=lambda q: q[0] ^ q[1],
            )
        )

    def complement(self):
        """
        Set complement of the interval set.
        """
        return IntervalSet.all().difference(self)

    @staticmethod
    def empty():
        """
        Create the empty set.
        """
        return IntervalSet([])

    @staticmethod
    def open(value_begin, value_end):
        """
        Create an open interval set with finite boundaries.
        """
        return IntervalSet([Interval.open(value_begin, value_end)])

    @staticmethod
    def closed(value_begin, value_end):
        """
        Create a closed interval set with finite boundaries.
        """
        return IntervalSet([Interval.closed(value_begin, value_end)])

    @staticmethod
    def point(value):
        """
        Create a zero-length degenerate [x, x] point-line 'interval set'.
        """
        return IntervalSet([Interval.point(value)])

    @staticmethod
    def low_slice(value_end, included=False):
        """
        Create an interval set from -inf to a certain value.
        """
        return IntervalSet([Interval.low_slice(value_end, included=included)])

    @staticmethod
    def high_slice(value_begin, included=False):
        """
        Create an interval set from a value up to +inf.
        """
        return IntervalSet([Interval.high_slice(value_begin, included=included)])

    @staticmethod
    def all():
        """
        Return the "whole of it" interval set.
        """
        return IntervalSet([Interval.all()])

    @staticmethod
    def interval(value_begin, begin_included, value_end, end_included):
        """
        Directly create an interval set from the values
        and the open/closed specs.
        """
        return IntervalSet([Interval.interval(
            value_begin,
            begin_included,
            value_end,
            end_included,
        )])
