"""
Defines symbols for extension to +/- infinity and related methods.
"""

from clothesline.exceptions import IndeterminateFormError, UnparseableDictError


class PlusInf:  # noqa: PLR0903
    """
    Symbolic constant for "+infinity"
    """

    @staticmethod
    def __repr__():
        return "+inf"


class MinusInf:  # noqa: PLR0903
    """
    Symbolic constant for "-infinity"
    """

    @staticmethod
    def __repr__():
        return "-inf"


def is_symbol(value):
    """
    Return True if the value is a symbolic constant.
    """
    return value is PlusInf or value is MinusInf


def x_repr(val):
    """
    String representation
    """
    if is_symbol(val):  # noqa: PLR1705
        return val.__repr__()
    else:
        return val.__repr__()


def x_to_dict(value, v_encoder):
    """
    Return a json-encodable representation of this extended 'value'.
    """
    if is_symbol(value):  # noqa: PLR1705
        return {"symbol": value.__repr__()}
    else:
        # "ordinary value"
        return {"o_value": v_encoder(value)}


def x_from_dict(input_dict, v_decoder):
    """
    Extract a extended value from a dictionary item, leveraging the passed
    decoder.
    """
    if "symbol" in input_dict:  # noqa: PLR1705
        if input_dict["symbol"] == PlusInf.__repr__():  # noqa: PLR1705
            return PlusInf
        elif input_dict["symbol"] == MinusInf.__repr__():
            return MinusInf
        else:
            raise UnparseableDictError
    else:
        return v_decoder(input_dict["o_value"])


# Extensions of arithmetic to "domain + infinities"


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
    if x_equals(val1, val2):  # noqa: PLR1705
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


def x_sum(val1, val2, adder):  # noqa: PLR0911
    """
    Sum of two values.
    Will raise an error if the two values are the two (opposite) infinities
    """
    if val1 is PlusInf:  # noqa: PLR1705
        if val2 is PlusInf:  # noqa: PLR1705
            # +inf + +inf
            return PlusInf
        elif val2 is MinusInf:
            # +inf + -inf
            raise IndeterminateFormError
        else:
            # +inf + num
            return PlusInf
    elif val1 is MinusInf:
        if val2 is PlusInf:  # noqa: PLR1705, PLR1720
            # -inf + +inf
            raise IndeterminateFormError
        elif val2 is MinusInf:
            # -inf + -inf
            return MinusInf
        else:
            # -inf + num
            return MinusInf
    else:
        if val2 is PlusInf:  # noqa: PLR1705
            # num + +inf
            return PlusInf
        elif val2 is MinusInf:
            # num + -inf
            return MinusInf
        else:
            # num + num
            return adder(val1, val2)


def x_subtract(val1, val2, subtracter):  # noqa: PLR0911
    """
    Evaluate the difference val1 - val2.
    Will raise an error if indeterminate forms arise.
    """
    if val1 is PlusInf:  # noqa: PLR1705
        if val2 is PlusInf:  # noqa: PLR1705, PLR1720
            # +inf - +inf
            raise IndeterminateFormError
        elif val2 is MinusInf:
            # +inf - -inf
            return PlusInf
        else:
            # +inf - num
            return PlusInf
    elif val1 is MinusInf:
        if val2 is PlusInf:  # noqa: PLR1705
            # -inf - +inf
            return MinusInf
        elif val2 is MinusInf:
            # -inf - -inf
            raise IndeterminateFormError
        else:
            # -inf - num
            return MinusInf
    else:
        if val2 is PlusInf:  # noqa: PLR1705
            # num - +inf
            return MinusInf
        elif val2 is MinusInf:
            # num - -inf
            return PlusInf
        else:
            # num - num
            return subtracter(val1, val2)
