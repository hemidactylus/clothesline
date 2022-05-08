from clothesline.exceptions import InvalidValueError

from clothesline.symbols import isSymbol
from clothesline.symbols import xEquals, xGt, xLt

class IntervalPeg():
    value = None
    included = None

    def __init__(self, value, included):
        self.value = value
        if isSymbol(self.value) and included:
            raise InvalidValueError('Infinities cannot be included in peg')
        self.included = included

    def __eq__(self, other):
        return xEquals(self.value, other.value) and self.included == other.included

    def __gt__(self, other):
        """
        If same value, we consider that included comes "after" excluded
        """
        if xGt(self.value, other.value):
            return True
        elif xLt(self.value, other.value):
            return False
        else:
            if (not self.included) and other.included:
                return True
            else:
                return False

    def __ge__(self, other):
        return self == other or self > other
