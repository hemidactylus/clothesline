"""
"Metric kit" to equip the real-number interval/sets with extension.
This is prototypical of analogous augmentations to other intervals*/sets*
"""


class RealDomainMetric():
    """
    Metric definition for real numbers.
    """

    @staticmethod
    def adder(val1, val2): return val1 + val2  # noqa: PLC0116, PLC0321

    @staticmethod
    def subtracter(val1, val2): return val1 - val2  # noqa: PLC0116, PLC0321

    zero = 0
