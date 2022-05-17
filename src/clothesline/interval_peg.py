"""
A single value + indication of whether included or not in the interval it
contributes to defining.
"""

from clothesline.exceptions import InvalidValueError

from clothesline.symbols import is_symbol
from clothesline.symbols import x_equals


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
