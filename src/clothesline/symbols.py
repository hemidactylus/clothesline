class PLUS_INF():
    pass


class MINUS_INF():
    pass


def isSymbol(value):
    return value is PLUS_INF or value is MINUS_INF


# extensions of in/equality comparisons to R+infinities:

def xEquals(v1, v2):
    if v1 is PLUS_INF:
        return v2 is PLUS_INF
    elif v1 is MINUS_INF:
        return v2 is MINUS_INF
    else:
        return v1 == v2

def xGt(v1, v2):
    if v1 is PLUS_INF:
        return not (v2 is PLUS_INF)
    elif v1 is MINUS_INF:
        return False
    else:
        # v1 is a regular number:
        if v2 is PLUS_INF:
            return False
        elif v2 is MINUS_INF:
            return True
        else:
            # both are numbers
            return v1 > v2

def xLt(v1, v2):
    return xGt(v2, v1)

def xGe(v1, v2):
    return xEquals(v1, v2) or xGt(v1, v2)

def xLe(v1, v2):
    return xEquals(v1, v2) or xLt(v1, v2)
