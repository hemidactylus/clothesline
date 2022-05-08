"""
A single interval with a begin and and end, either open or closed at its ends.
"""

from clothesline import IntervalPeg
from clothesline.symbols import PlusInf, MinusInf
from clothesline.symbols import is_symbol, x_equals, x_lt

#
from clothesline.exceptions import InvalidValueError


class Interval:
    """
    A single uninterrupted interval over the universe field:
        [a,b] or (a,b) or (a,b] or [a,b)
    defined by two IntervalPeg objects. It can span to infinities.
    """

    begin = None
    end = None

    def __init__(self, begin, end):
        """
        begin and end are PegInterval instances
        """
        if begin > end:
            raise InvalidValueError("Interval begin must come before its end")
        self.begin = begin
        self.end = end

    def contains(self, value):  # noqa: PLR0911
        """
        Test whether a value belongs to the interval.

        Infinities are allowed as 'value' argument
        and e.g. conventionally (-INF, 0] contains -INF (and so on)
        """
        if is_symbol(value):
            if value is PlusInf:  # noqa: PLR1705
                return x_equals(self.end.value, value)
            else:
                return x_equals(self.begin.value, value)
        else:
            # value is a regular number:
            if x_lt(self.begin.value, value):
                # value to the right of begin
                if x_lt(value, self.end.value):  # noqa: PLR1705
                    # value to the left of end
                    return True
                else:
                    # value to the right, or equal to, end
                    if x_equals(self.end.value, value):  # noqa: PLR1705
                        # value sits at end
                        return self.end.included
                    else:
                        # value to the right of end
                        return False
            else:
                # value to the left, or equal to begin
                if x_equals(self.begin.value, value):  # noqa: PLR1705
                    # value sits at begin
                    return self.begin.included
                else:
                    # value to the left of begin
                    return False

    def __eq__(self, other):
        return self.begin == other.begin and self.end == other.end

    @staticmethod
    def open(value_begin, value_end):
        """
        Create an open interval with finite boundaries.
        """
        return Interval.interval(
            value_begin,
            False,
            value_end,
            False,
        )

    @staticmethod
    def closed(value_begin, value_end):
        """
        Create a closed interval with finite boundaries.
        """
        return Interval.interval(
            value_begin,
            True,
            value_end,
            True,
        )

    @staticmethod
    def low_slice(value_end, included=False):
        """
        Create an interval from -inf to a certain value.
        """
        return Interval.interval(
            MinusInf,
            False,
            value_end,
            included,
        )

    @staticmethod
    def high_slice(value_begin, included=False):
        """
        Create an interval from a value up to +inf.
        """
        return Interval.interval(
            value_begin,
            included,
            PlusInf,
            False,
        )

    @staticmethod
    def all():
        """
        Return the "whole of it" interval.
        """
        return Interval.interval(
            MinusInf,
            False,
            PlusInf,
            False,
        )

    @staticmethod
    def interval(value_begin, begin_included, value_end, end_included):
        """
        Directly create an interval from the values and the open/closed specs.
        """
        return Interval(
            IntervalPeg(value_begin, begin_included),
            IntervalPeg(value_end, end_included),
        )
