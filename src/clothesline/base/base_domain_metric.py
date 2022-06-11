"""
Metric specification for an interval/set.
"""


class BaseDomainMetric:
    """
    Abstract class for creating 'metric' static classes,
    which prescribe how to deal with the concept of interval "length" and
    their summations.
    """

    def __init__(self):
        raise RuntimeError("This class is static.")

    @staticmethod
    def adder(val1, val2):  # noqa: PLW0613
        """How to add two 'extensions' to get another 'extension'."""

    @staticmethod
    def subtracter(val1, val2):  # noqa: PLW0613
        """
        How to subtract two ends of an interval (peg values)
        to get its 'extension'.
        """

    """What is the 'zero extension' when computing the extension of a set."""  # noqa: PLW0105, E501
    zero = ...
