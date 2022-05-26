"""
A class containing the "interface" for creation ex-novo of intervalsets*,
with the key feature that the actual class to instantiate when creating these
is set upon creation of the IntervalSetGenericUtils instance.
In this way, a "utils" object can be spawned by IntervalSets or analogous
classes and with a common set of methods an "utils" creates intervalsets
of the appropriate type.
"""

from clothesline.interval import Interval


class IntervalSetGenericUtils:

    def __init__(self, interval_set_class):
        """
        An instance of IntervalSetGenericUtils needs to know what class
        to use to create intervalsets*.
        """
        self.interval_set_class = interval_set_class

    def empty(self):
        """
        Create the empty set.
        """
        return self.interval_set_class([])

    def open(self, value_begin, value_end):
        """
        Create an open interval set with finite boundaries.
        """
        return self.interval_set_class([Interval.open(value_begin, value_end)])

    def closed(self, value_begin, value_end):
        """
        Create a closed interval set with finite boundaries.
        """
        return self.interval_set_class([Interval.closed(value_begin, value_end)])

    def point(self, value):
        """
        Create a zero-length degenerate [x, x] point-line 'interval set'.
        """
        return self.interval_set_class([Interval.point(value)])

    def low_slice(self, value_end, included=False):
        """
        Create an interval set from -inf to a certain value.
        """
        return self.interval_set_class([Interval.low_slice(value_end, included=included)])

    def high_slice(self, value_begin, included=False):
        """
        Create an interval set from a value up to +inf.
        """
        return self.interval_set_class([Interval.high_slice(value_begin, included=included)])

    def all(self):
        """
        Return the "whole of it" interval set.
        """
        return self.interval_set_class([Interval.all()])

    def interval(self, value_begin, begin_included, value_end, end_included):
        """
        Directly create an interval set from the values
        and the open/closed specs.
        """
        return self.interval_set_class([Interval.interval(
            value_begin,
            begin_included,
            value_end,
            end_included,
        )])
