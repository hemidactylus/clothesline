"""
A single value + indication of whether included or not in the interval it
contributes to defining.

In the chain IntervalPeg -> Interval -> IntervalSet, the peg is the only
level that is a single class unambiguously. It will not receive the context
dependencies that make Interval* and IntervalSet* a "family" of classes.
"""

from clothesline.algebra.symbols import is_symbol, x_to_dict
from clothesline.algebra.symbols import x_equals
#
from clothesline.exceptions import InvalidValueError


class IntervalPeg:
    """
    A boundary value + indication of whether the value itself is
    included/excluded.

    Note: inequalities among instances of this class make no sense,
    whereas they do among their 'value' values.
    """

    value = None
    included = None

    def __init__(self, value, included):
        self.value = value
        if is_symbol(self.value) and included:
            raise InvalidValueError("Infinities cannot be included in peg")
        self.included = included

    def __eq__(self, other):
        if x_equals(self.value, other.value):  # noqa: PLR1705
            return self.included == other.included
        else:
            return False

    def __hash__(self):
        return hash((self.value, self.included))

    def to_dict(self, v_encoder):
        """
        Return a json-encodable representation of this peg.
        """
        return {
            'value': x_to_dict(self.value, v_encoder=v_encoder),
            'included': self.included,
        }
