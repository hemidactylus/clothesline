"""
An arbitrary set defined by a finite number of intervals.
"""

from clothesline.algebra import combine_intervals


class IntervalSet:
    """
    A portion of the continuous line (e.g. the reals + infinities)
    defined by an arbitrary (finite) number of Interval objects.
    """

    intervals = None

    def __init__(self, intervals):
        """`intervals` is a list of Interval instances."""
        self.intervals = self._normalize(intervals)

    def contains(self, value):
        """
        Test whether a value belongs to the set.

        Conventionally, infinities do not belong to any interval set.
        """
        return any(interval.contains(value) for interval in self.intervals)

    def __eq__(self, other):
        return (
            len(self.intervals) == len(other.intervals)
            and self.intervals == other.intervals
        )

    def __hash__(self, other):
        raise NotImplementedError

    def __repr__(self):
        if self.intervals == []:
            return "{}"
        else:
            return " U ".join(interval.__repr__() for interval in self.intervals)

    @staticmethod
    def _normalize(intervals):
        """
        An arbitrary input of intervals (overlapping, unsorted)
        is reduced to 'normal form' using the one-single-list
        form of the generic combiner.
        """
        return combine_intervals([intervals])

    def __add__(self, other):
        return IntervalSet(
            combine_intervals(
                [self.intervals, other.intervals],
                combiner_function=lambda q: q[0] or q[1],
            )
        )
