"""
A class containing the "interface" for creation ex-novo of intervalsets*,
with the key feature that the actual class to instantiate when creating these
is set upon creation of the IntervalSetGenericUtils instance.
In this way, a "utils" object can be spawned by IntervalSets or analogous
classes and with a common set of methods an "utils" creates intervalsets
of the appropriate type.
"""

from clothesline.exceptions import (
    UnparseableDictError,
    UnserializableItemError,
    UnsupportedVersionDictError,
)


class IntervalSetGenericUtils:
    """
    An "interval set utils" class. Instances are able to use the provided
    'name of an interval set class' and create standard out-of-the-box
    intervals.
    """

    def __init__(self, interval_set_class):
        """
        An instance of IntervalSetGenericUtils needs to know what class
        to use to create intervalsets* (and intervals*).
        From this knowledge, all other properties and instantiators
        are crafted internally (also to create the right type of objects).
        """
        interval_class = interval_set_class.interval_class
        self.set_instantiator = interval_set_class
        # the above would be: lambda intervals: interval_set_class(intervals)
        self.int_utils = interval_class.utils()
        self.serializing_class = interval_set_class.serializing_class
        self.serializing_version = interval_set_class.serializing_version

    def from_dict(self, input_dict):
        """
        Extract an instance of this interval set from a dict,
        using the provided serializability settings
        (including checking dict metadata match).
        """
        if self.serializing_class is None or self.serializing_version is None:
            raise UnserializableItemError
        #
        if input_dict.get("class") != self.serializing_class:
            raise UnparseableDictError
        # Here, in the future, version upgrade logic will be injected
        if input_dict.get("version", 0) > self.serializing_version:
            raise UnsupportedVersionDictError
        if input_dict.get("version") != self.serializing_version:
            raise UnparseableDictError
        #
        return self.set_instantiator(
            self.int_utils.from_dict(interval_dict)
            for interval_dict in input_dict["intervals"]
        )

    def empty(self):
        """
        Create the empty set.
        """
        return self.set_instantiator([])

    def open(self, value_begin, value_end):
        """
        Create an open interval set with finite boundaries.
        """
        return self.set_instantiator(
            [self.int_utils.open(value_begin, value_end)],
        )

    def closed(self, value_begin, value_end):
        """
        Create a closed interval set with finite boundaries.
        """
        return self.set_instantiator(
            [self.int_utils.closed(value_begin, value_end)],
        )

    def point(self, value):
        """
        Create a zero-length degenerate [x, x] point-line 'interval set'.
        """
        return self.set_instantiator([self.int_utils.point(value)])

    def low_slice(self, value_end, included=False):
        """
        Create an interval set from -inf to a certain value.
        """
        return self.set_instantiator(
            [self.int_utils.low_slice(value_end, included=included)],
        )

    def high_slice(self, value_begin, included=False):
        """
        Create an interval set from a value up to +inf.
        """
        return self.set_instantiator(
            [self.int_utils.high_slice(value_begin, included=included)],
        )

    def all(self):
        """
        Return the "whole of it" interval set.
        """
        return self.set_instantiator([self.int_utils.all()])

    def interval(self, value_begin, begin_included, value_end, end_included):
        """
        Directly create an interval set from the values
        and the open/closed specs.
        """
        return self.set_instantiator(
            [
                self.int_utils.interval(
                    value_begin,
                    begin_included,
                    value_end,
                    end_included,
                )
            ]
        )
