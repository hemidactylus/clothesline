"""
A single value + indication of whether included or not in the interval it
contributes to defining.
"""

from clothesline.exceptions import InvalidValueError

from clothesline.symbols import is_symbol
from clothesline.symbols import x_equals, x_gt, x_lt


class IntervalPeg:
    """
    A boundary value + indication of whether the value itself is
    included/excluded.
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

    def __gt__(self, other):
        """
        If same value, we consider that included comes "after" excluded
        """
        if x_gt(self.value, other.value):  # noqa: PLR1705
            return True
        elif x_lt(self.value, other.value):
            return False
        else:
            if (not self.included) and other.included:  # noqa: PLR1703,PLR1705
                return True
            else:
                return False

    def __ge__(self, other):
        return self == other or self > other
