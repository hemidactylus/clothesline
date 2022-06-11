"""
One of the two ends of an interval.

A single value + indication of whether included or not in the interval it
contributes to defining.

In the chain IntervalPeg -> Interval* -> IntervalSet*, the peg is the only
level that is not subclassed/enriched. It receives the context it needs
(e.g. a codec pair) in individual calls as the peg is not indended for use
by outside of this library.
"""

from clothesline.algebra.symbols import is_symbol, x_to_dict, x_from_dict
from clothesline.algebra.symbols import x_equals

#
from clothesline.exceptions import InvalidValueError


class IntervalPeg:
    """
    A boundary value + indication of whether the value itself is
    included/excluded.

    Note: greater/lesser inequalities among instances of this class make
    no sense, whereas they do among their 'value' values.
    """

    def __init__(self, value, included):
        self.value = value
        if is_symbol(self.value) and included:
            raise InvalidValueError("Infinities cannot be included in peg")
        self.included = included

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if x_equals(self.value, other.value):  # noqa: PLR1705
                return self.included == other.included
            else:
                return False
        else:
            return False

    def __hash__(self):
        return hash((self.value, self.included))

    def to_dict(self, v_encoder):
        """
        Return a json-encodable representation of this peg.
        An encoder for the regular domain values is required.
        """
        return {
            "value": x_to_dict(self.value, v_encoder=v_encoder),
            "included": self.included,
        }

    @staticmethod
    def from_dict(input_dict, v_decoder):
        """
        Parse a dict-representation of a peg and return it as a peg.
        A decoder for the regular domain values is required.
        """
        return IntervalPeg(
            x_from_dict(input_dict["value"], v_decoder=v_decoder),
            input_dict["included"],
        )
