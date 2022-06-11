"""
Abstract class for defining 'metric' static classes,
which prescribe how to deal with interval "length" and their summations.
"""

class BaseDomainMetric():

    def __init__(self):
        raise NotImplementedError('This class is static.')

    def adder(v1, v2): ...

    def subtracter(v1, v2): ...

    zero = ...
