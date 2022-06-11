"""
Specific exceptions for clothesline objects.
"""


class InvalidValueError(ValueError):
    """
    An attempt to build an object (e.g. IntervalPeg) with invalid
    or inconsistent values.
    """


class InvalidCombineEndState(ValueError):
    """
    An end state when closing the ''combine_intervals'
    with an unterminated open buffer to flush.
    """


class IndeterminateFormError(ValueError):
    """
    An indeterminate form arisen through operations
    involving symbols (e.g. "infinity - infinity")
    """


class MetricNotImplementedError(ValueError):
    """
    An interval*/intervalset* class is asked to do
    metric computations, but no metric is defined.
    """


class UnserializableItemError(ValueError):
    """
    An attempt to convert an interval*/set* to json is made
    for an object whose domain data type admits no serializable form.
    """


class UnparseableDictError(ValueError):
    """
    An attempt to parse an invalid dict back to an interval* or intervalset*
    """


class UnsupportedVersionDictError(ValueError):
    """
    The version of this dict is too new to be hydrated back to an object.
    """
