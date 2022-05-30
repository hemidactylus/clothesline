"""
Specific exceptions for the project.
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
