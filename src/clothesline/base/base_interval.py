"""
A single interval with a begin and and end, either open or closed at its ends.
"""

from clothesline.algebra.symbols import (
    is_symbol,
    x_equals,
    x_lt,
    x_gt,
    x_repr,
    x_subtract,
)

#
from clothesline.exceptions import (
    InvalidValueError,
    MetricNotImplementedError,
    UnserializableItemError,
)


class BaseInterval:
    """
    A single uninterrupted interval over the domain field:
    [a,b] or (a,b) or (a,b] or [a,b)
    defined by two IntervalPeg objects. It can span to infinities.

    Concrete classes must provide builder() and utils() in a standard way
    (see the real-interval case) and, if desired,
    define metric and serializability properties as well.
    """

    # What follows should be considered by subclassers:

    metric = None

    value_encoder = None
    value_decoder = None

    serializing_class = None
    serializing_version = None

    @staticmethod
    def builder():
        """Create and return a "builder" for these intervals."""

    @staticmethod
    def utils():
        """Create an "interval utils" object for these intervals."""

    # Subclassers may stop reading here.

    def __init__(self, begin, end):
        """
        begin and end are IntervalPeg instances
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
        if isinstance(other, self.__class__):  # noqa: PLR1705
            return self.begin == other.begin and self.end == other.end
        else:
            return False

    def __hash__(self):
        return hash((self.__class__, hash(self.begin), hash(self.end)))

    def __repr__(self):
        begin_name = x_repr(self.begin.value)
        begin_paren = "[" if self.begin.included else "("
        end_name = x_repr(self.end.value)
        end_paren = "]" if self.end.included else ")"
        return f"{begin_paren}{begin_name}, {end_name}{end_paren}"

    def to_dict(self):
        """
        Return a json-encodable representation of this interval.
        """
        if self.value_encoder:  # noqa: PLR1705
            return {
                "class": self.serializing_class,
                "version": self.serializing_version,
                "pegs": [
                    self.begin.to_dict(v_encoder=self.value_encoder),
                    self.end.to_dict(v_encoder=self.value_encoder),
                ],
            }
        else:
            raise UnserializableItemError

    def contains(self, value):  # noqa: PLR0911
        """
        Test whether a value belongs to the interval.

        Infinities are allowed as 'value' argument, but never belong.
        """
        if is_symbol(value):  # noqa: PLR1705
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

    def extension(self):
        """
        If a metric is defined for this interval type,
        use it to compute this interval's 'extension'.
        """
        if self.metric:  # noqa: PLR1705
            return x_subtract(
                self.end.value,
                self.begin.value,
                subtracter=self.metric.subtracter,
            )
        else:
            raise MetricNotImplementedError

    def pegs(self):
        """Return the two ends, iterably."""
        yield self.begin
        yield self.end

    def intervals(self):
        """
        Return an 'iterable' over a single element, this interval.
        This is only to enable quick-syntax for those IntervalSet
        set-wise operations whereby the second operand is a puny Interval.
        """
        yield self
