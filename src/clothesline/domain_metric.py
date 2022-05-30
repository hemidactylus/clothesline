"""
Metric kit to augment Interval and IntervalSet,
prototypical of analogous augmentations to other intervals*/sets*
"""

class DomainMetric():

    def __init__(self):
        raise NotImplementedError('This class is static.')

    def adder(v1, v2): return v1 + v2

    def subtracter(v1, v2): return v1 - v2

    zero = 0
