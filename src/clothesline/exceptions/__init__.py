"""
Specific exceptions for the project.
"""


class InvalidValueError(ValueError):
    """
    An attempt to build an object (e.g. IntervalPeg) with invalid
    or inconsistent values.
    """
