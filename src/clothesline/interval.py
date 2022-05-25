"""
A single interval with a begin and and end, either open or closed at its ends.
"""

from clothesline import IntervalPeg
from clothesline.symbols import PlusInf, MinusInf
from clothesline.symbols import is_symbol, x_equals, x_lt, x_gt, x_repr
from clothesline.interval_generic_builder import IntervalGenericBuilder
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
        if x_gt(begin.value, end.value):
            raise InvalidValueError("Interval begin must come before its end")
        if x_equals(begin.value, end.value):
            if begin.included != end.included:
                raise InvalidValueError(
                    "Contradicting inclusion for point-like interval"
                )
            if not begin.included and not end.included:
                raise InvalidValueError("Empty point-like open set is invalid")
        self.begin = begin
        self.end = end

    def __eq__(self, other):
        if isinstance(other, Interval):
            return self.begin == other.begin and self.end == other.end
        else:
            return False

    def __hash__(self):
        return hash((self.begin, self.end))

    def __repr__(self):
        beginName = x_repr(self.begin.value)
        beginParen = "[" if self.begin.included else "("
        endName = x_repr(self.end.value)
        endParen = "]" if self.end.included else ")"
        return f"{beginParen}{beginName}, {endName}{endParen}"

    def contains(self, value):  # noqa: PLR0911
        """
        Test whether a value belongs to the interval.

        Infinities are allowed as 'value' argument, but never belong.
        """
        if is_symbol(value):
            return False
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

    def pegs(self):
        """Return the two ends, iterably."""
        yield self.begin
        yield self.end

    def intervals(self):
        """
        Return an 'iterable' over a single element, this interval.
        This is only to enable quick-syntax for IntervalSet set-wise operations
        whereby the second operand is a puny Interval.
        """
        yield self

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
    def point(value):
        """
        Create a zero-length degenerate [x, x] point-line 'interval'.
        """
        return Interval.closed(value, value)

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

    @staticmethod
    def builder():
        return IntervalGenericBuilder(finalizer=lambda pegs: Interval(*pegs))
