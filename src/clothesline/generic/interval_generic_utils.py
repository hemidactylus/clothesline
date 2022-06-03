"""
A class containing the "interface" for creation of intervals*, (not 'sets').
Like for the IntervalSetGenericUtils, the actual class to instantiate
is set per-instance, so this serves as a generic class template.
"""

from clothesline.interval_peg import IntervalPeg
from clothesline.algebra.symbols import PlusInf, MinusInf

from clothesline.exceptions import UnparseableDictError, UnserializableItemError, UnsupportedVersionDictError


class IntervalGenericUtils:

    def __init__(self, int_instantiator, value_decoder=None, serializing_class=None, serializing_version=None):
        """
        When creating an utils instance, which can create intervals*,
        the instantiator that must be passed is a function that makes
        its two arguments (peg0, peg1) into an interval of the desired type.
        """
        self.int_instantiator = int_instantiator
        self.value_decoder = value_decoder
        self.serializing_class = serializing_class
        self.serializing_version = serializing_version

    def from_dict(self, input_dict):
        if not self.value_decoder:
            raise UnserializableItemError
        if input_dict.get('class') != self.serializing_class:
            raise UnparseableDictError
        # Here, in the future, version upgrade logic will be injected
        if input_dict.get('version', 0) > self.serializing_version:
            raise UnsupportedVersionDictError
        if input_dict.get('version') != self.serializing_version: 
            raise UnparseableDictError
        return self.int_instantiator(
            IntervalPeg.from_dict(input_dict['pegs'][0], v_decoder=self.value_decoder),
            IntervalPeg.from_dict(input_dict['pegs'][1], v_decoder=self.value_decoder),
        )

    def open(self, value_begin, value_end):
        """
        Create an open interval with finite boundaries.
        """
        return self.interval(
            value_begin,
            False,
            value_end,
            False,
        )

    def closed(self, value_begin, value_end):
        """
        Create a closed interval with finite boundaries.
        """
        return self.interval(
            value_begin,
            True,
            value_end,
            True,
        )

    def point(self, value):
        """
        Create a zero-length degenerate [x, x] point-line 'interval'.
        """
        return self.closed(value, value)

    def low_slice(self, value_end, included=False):
        """
        Create an interval from -inf to a certain value.
        """
        return self.interval(
            MinusInf,
            False,
            value_end,
            included,
        )

    def high_slice(self, value_begin, included=False):
        """
        Create an interval from a value up to +inf.
        """
        return self.interval(
            value_begin,
            included,
            PlusInf,
            False,
        )

    def all(self, ):
        """
        Return the "whole of it" interval.
        """
        return self.interval(
            MinusInf,
            False,
            PlusInf,
            False,
        )

    def interval(self, value_begin, begin_included, value_end, end_included):
        """
        Directly create an interval from the values and the open/closed specs.
        """
        return self.int_instantiator(
            IntervalPeg(value_begin, begin_included),
            IntervalPeg(value_end, end_included),
        )
