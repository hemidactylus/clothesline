"""
A class containing the "interface" for creation ex-novo of intervalsets*,
with the key feature that the actual class to instantiate when creating these
is set upon creation of the IntervalSetGenericUtils instance.
In this way, a "utils" object can be spawned by IntervalSets or analogous
classes and with a common set of methods an "utils" creates intervalsets
of the appropriate type.
"""


class IntervalSetGenericUtils:

    def __init__(self, set_instantiator, int_utils):
        """
        An instance of IntervalSetGenericUtils needs to know what class
        to use to create intervalsets*.
        """
        self.set_instantiator = set_instantiator
        self.int_utils = int_utils

    def empty(self):
        """
        Create the empty set.
        """
        return self.set_instantiator([])

    def open(self, value_begin, value_end):
        """
        Create an open interval set with finite boundaries.
        """
        return self.set_instantiator([self.int_utils.open(value_begin, value_end)])

    def closed(self, value_begin, value_end):
        """
        Create a closed interval set with finite boundaries.
        """
        return self.set_instantiator([self.int_utils.closed(value_begin, value_end)])

    def point(self, value):
        """
        Create a zero-length degenerate [x, x] point-line 'interval set'.
        """
        return self.set_instantiator([self.int_utils.point(value)])

    def low_slice(self, value_end, included=False):
        """
        Create an interval set from -inf to a certain value.
        """
        return self.set_instantiator([self.int_utils.low_slice(value_end, included=included)])

    def high_slice(self, value_begin, included=False):
        """
        Create an interval set from a value up to +inf.
        """
        return self.set_instantiator([self.int_utils.high_slice(value_begin, included=included)])

    def all(self):
        """
        Return the "whole of it" interval set.
        """
        return self.set_instantiator([self.int_utils.all()])

    def interval(self, value_begin, begin_included, value_end, end_included):
        """
        Directly create an interval set from the values
        and the open/closed specs.
        """
        return self.set_instantiator([self.int_utils.interval(
            value_begin,
            begin_included,
            value_end,
            end_included,
        )])
