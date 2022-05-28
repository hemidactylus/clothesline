"""
A class containing the "interface" for creation of intervals*, (not 'sets').
Like for the IntervalSetGenericUtils, the actual class to instantiate
is set per-instance, so this serves as a generic class template.
"""

from clothesline.interval_peg import IntervalPeg
from clothesline.algebra.symbols import PlusInf, MinusInf


class IntervalGenericUtils:

    def __init__(self, int_instantiator):
        """
        When creating an utils instance, which can create intervals*,
        the instantiator that must be passed is a function that makes
        its two arguments (peg0, peg1) into an interval of the desired type.
        """
        self.int_instantiator = int_instantiator

    def open(self, value_begin, value_end):
        """
        Create an open interval with finite boundaries.
        """
        return self.interval(
            value_begin,
            False,
            value_end,
            False,
        )

    def closed(self, value_begin, value_end):
        """
        Create a closed interval with finite boundaries.
        """
        return self.interval(
            value_begin,
            True,
            value_end,
            True,
        )

    def point(self, value):
        """
        Create a zero-length degenerate [x, x] point-line 'interval'.
        """
        return self.closed(value, value)

    def low_slice(self, value_end, included=False):
        """
        Create an interval from -inf to a certain value.
        """
        return self.interval(
            MinusInf,
            False,
            value_end,
            included,
        )

    def high_slice(self, value_begin, included=False):
        """
        Create an interval from a value up to +inf.
        """
        return self.interval(
            value_begin,
            included,
            PlusInf,
            False,
        )

    def all(self, ):
        """
        Return the "whole of it" interval.
        """
        return self.interval(
            MinusInf,
            False,
            PlusInf,
            False,
        )

    def interval(self, value_begin, begin_included, value_end, end_included):
        """
        Directly create an interval from the values and the open/closed specs.
        """
        return self.int_instantiator(
            IntervalPeg(value_begin, begin_included),
            IntervalPeg(value_end, end_included),
        )
