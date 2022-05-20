"""
Defines symbols for extension to +/- infinity and related methods.
"""


class PlusInf:  # noqa: PLR0903
    """
    Symbolic constant for "+infinity"
    """
    @staticmethod
    def __repr__(): return '+inf'


class MinusInf:  # noqa: PLR0903
    """
    Symbolic constant for "-infinity"
    """
    @staticmethod
    def __repr__(): return '-inf'


def is_symbol(value):
    """
    Return True if the value is a symbolic constant.
    """
    return value is PlusInf or value is MinusInf


# extensions of in/equality comparisons to R+infinities:


def x_equals(val1, val2):
    """
    Equality, extended
    """
    if val1 is PlusInf:  # noqa: PLR1705
        return val2 is PlusInf
    elif val1 is MinusInf:
        return val2 is MinusInf
    else:
        return val1 == val2


def x_gt(val1, val2):
    """
    Greater-than, extended
    """
    if val1 is PlusInf:  # noqa: PLR1705
        return val2 is not PlusInf
    elif val1 is MinusInf:
        return False
    else:
        # val1 is a regular number:
        if val2 is PlusInf:  # noqa: PLR1705
            return False
        elif val2 is MinusInf:
            return True
        else:
            # both are numbers
            return val1 > val2


def x_lt(val1, val2):
    """
    Less-than, extended
    """
    return x_gt(val2, val1)  # noqa: PLW1114


def x_cmp(val1, val2):
    """
    a valid 'cmp' to use for sorting values-and-symbols
    """
    if x_equals(val1, val2):
        return 0
    else:
        return -1 if x_lt(val1, val2) else +1


def x_ge(val1, val2):
    """
    Greater-or-equal, extended
    """
    return x_equals(val1, val2) or x_gt(val1, val2)


def x_le(val1, val2):
    """
    Less-or-equal, extended
    """
    return x_equals(val1, val2) or x_lt(val1, val2)

def x_repr(val):
    """
    String representation
    """
    if is_symbol(val):
        return val.__repr__()
    else:
        return val.__repr__()
