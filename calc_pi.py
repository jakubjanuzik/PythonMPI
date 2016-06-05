# coding: utf-8
from decimal import Decimal, getcontext

PRECISION = 50
getcontext().prec = PRECISION
POW239 = [Decimal(1)]
POW5 = [Decimal(1)]


def initialize_powers():
    """
        Precomputing for calculating powers.
        Caching powers.
    """
    for i in xrange(1, PRECISION * 2 + 1):
        POW239.append(POW239[i - 1] * Decimal(239))
        POW5.append(POW5[i - 1] * Decimal(5))


def arctg239():
    """
        Szereg Talora dla arctg 239.
    """
    result = Decimal(0)
    for i in xrange(PRECISION):
        if i % 2 == 0:
            sign = 1
        else:
            sign = -1
        result += Decimal(sign) / (Decimal(2 * i + 1) * POW239[2 * i + 1])

    return result


def arctg5():
    """
        Szereg Taylora dla arctg 5.
        Możliwa niedokładność dla dwóch ostatnich liczb.
    """
    result = Decimal(0)
    for i in xrange(PRECISION):
        if i % 2 == 0:
            sign = 1
        else:
            sign = -1
        result += Decimal(sign) / (Decimal(2 * i + 1) * POW5[2 * i + 1])

    return result


def calc_pi():
    initialize_powers()
    arc_5 = arctg5()
    arc_239 = arctg239()
    return (Decimal(16) * arc_5 - Decimal(4) * arc_239)


if __name__ == '__main__':
    result = calc_pi()
    print result
