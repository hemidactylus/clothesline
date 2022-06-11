"""
"Metric kit" to equip the real-number interval/sets with extension.
This is prototypical of analogous augmentations to other intervals*/sets*
"""


class RealDomainMetric:
    """
    Metric definition for real numbers.
    """

    @staticmethod
    def adder(val1, val2):
        """The trivial adder."""
        return val1 + val2

    @staticmethod
    def subtracter(val1, val2):
        """The trivial subtracter."""
        return val1 - val2

    zero = 0
