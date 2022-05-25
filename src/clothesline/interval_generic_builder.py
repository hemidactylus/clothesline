"""
A utility to provide a "builder" interface for intervals, interval sets etc.
"""

from clothesline.symbols import PlusInf, MinusInf
from clothesline.interval_peg import IntervalPeg

class IntervalGenericBuilder():
    """
    TODO: write docstring
    """

    class _builder():

        def __init__(self, finalizer, begin):
            self._finalizer = finalizer
            self._begin = begin

        def _complete(self, value_end, included_end):
            if value_end is Ellipsis:
                _value_end = PlusInf
                _included_end = False
            else:
                _value_end = value_end
                _included_end = included_end
            end_peg = IntervalPeg(_value_end, _included_end)
            return self._finalizer([self._begin, end_peg])

        def __call__(self, value):
            return self._complete(value, False)

        def __getitem__(self, value):
            return self._complete(value, True)

    def __init__(self, finalizer):
        """
        Here additional context should be set.
        TO DOC
        """
        self._finalizer = finalizer

    def _start_building(self, value, included):
        """
        TO DOC
        """
        if value is Ellipsis:
            _value = MinusInf
            _included = False
        else:
            _value = value
            _included = included
        return self._builder(self._finalizer, IntervalPeg(_value, _included))

    def __call__(self, value):
        """Initiate interval building from an excluded initial peg."""
        return self._start_building(value, included=False)

    def __getitem__(self, value):
        """Initiate interval building from an included initial peg."""
        return self._start_building(value, included=True)
