"""
A utility to provide a "builder" interface for intervals, interval sets etc.
The actual class used to instantiate the interval* once completed is passed
when instantiating the builder: so, this "interface" can offer a standard
syntax yet result in the creation of intervals, interval sets and also
other types of intervalsets (e.g. enriched with metrics and so on).
"""

from clothesline.algebra.symbols import PlusInf, MinusInf
from clothesline.interval_peg import IntervalPeg

class IntervalGenericBuilder():
    """
    A builder for some kind of intervals.
    An instance of this class supports a [] and () syntax
    for specifying the first peg, an action which creates another object
    that waits for a "completion" call with () or [] and eventually
    results in creation of an interval*.
    """

    class _builder():
        """
        An internal volatile class used to represent, internally,
        states such as `builder(first_peg)`, i.e. ready to accept
        another [] or () and complete the sequence by creating
        an instance of (the appropriate class of) interval*.
        """

        def __init__(self, finalizer, begin):
            """a _builder knows the first peg and which finalizer to use."""
            self._finalizer = finalizer
            self._begin = begin

        def _complete(self, value_end, included_end):
            """
            Common call used behind the () and [] calls used to set
            the second peg thus completing the building.
            """
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
        When creating an IntervalGenericBuilder instance one passes
        a finalizer, i.e. a function from a 2-element list of pegs
        to the newly-created instance of interval*.

        Additional context is to be passed here (to be implemented).
        """
        self._finalizer = finalizer

    def _start_building(self, value, included):
        """
        Common call used behind the [] and () invocations, returns
        a _builder instance ready to accept the second peg of the interval.
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
