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
