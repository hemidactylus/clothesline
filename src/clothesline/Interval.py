from clothesline import IntervalPeg
from clothesline.symbols import PLUS_INF, MINUS_INF
from clothesline.symbols import isSymbol, xEquals, xGt, xLt
#
from clothesline.exceptions import InvalidValueError

class Interval():
    begin = None
    end = None

    def __init__(self, begin, end):
        """
        begin and end are PegInterval instances
        """
        if begin > end:
            raise InvalidValueError('Interval begin must come before its end')
        self.begin = begin
        self.end = end

    def contains(self, value):
        """
        Infinities are allowed as 'value' argument
        and e.g. conventionally (-INF, 0] contains -INF (and so on)
        """
        if isSymbol(value):
            if value is PLUS_INF:
                return xEquals(self.end.value, value)
            else:
                return xEquals(self.begin.value, value)
        else:
            # value is a regular number:
            if xLt(self.begin.value, value):
                # value to the right of begin
                if xLt(value, self.end.value):
                    # value to the left of end
                    return True
                else:
                    # value to the right, or equal to, end
                    if xEquals(self.end.value, value):
                        # value sits at end
                        return self.end.included
                    else:
                        # value to the right of end
                        return False
            else:
                # value to the left, or equal to begin
                if xEquals(self.begin.value, value):
                    # value sits at begin
                    return self.begin.included
                else:
                    # value to the left of begin
                    return False

    def __eq__(self, other):
        return self.begin == other.begin and self.end == other.end

    @staticmethod
    def Open(valueBegin, valueEnd):
        return Interval.Interval(
            valueBegin, False,
            valueEnd, False,
        )

    @staticmethod
    def Closed(valueBegin, valueEnd):
        return Interval.Interval(
            valueBegin, True,
            valueEnd, True,
        )

    @staticmethod
    def LowSlice(valueEnd, included=False):
        return Interval.Interval(
            MINUS_INF, False,
            valueEnd, included,
        )

    @staticmethod
    def HighSlice(valueBegin, included=False):
        return Interval.Interval(
            valueBegin, included,
            PLUS_INF, False,
        )

    @staticmethod
    def All():
        return Interval.Interval(
            MINUS_INF, False,
            PLUS_INF, False,
        )

    @staticmethod
    def Interval(valueBegin, beginIncluded, valueEnd, endIncluded):
        return Interval(
            IntervalPeg(valueBegin, beginIncluded),
            IntervalPeg(valueEnd, endIncluded),
        )
