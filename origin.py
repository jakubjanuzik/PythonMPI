from decimal import Decimal, getcontext

PRECISION = 1000
getcontext().prec = PRECISION
POW239 = [Decimal(1)]
POW5 = [Decimal(1)]

for i in xrange(1, PRECISION * 2 + 1):
    POW239.append(POW239[i - 1] * Decimal(239))
    POW5.append(POW5[i - 1] * Decimal(5))


def arctg239(x):
    result = Decimal(0)
    for i in xrange(PRECISION):
        if i % 2 == 0:
            sign = 1
        else:
            sign = -1
        result += Decimal(sign) / (Decimal(2 * i + 1) * POW239[2 * i + 1])

    return result


def arctg5(x):
    result = Decimal(0)
    for i in xrange(PRECISION):
        if i % 2 == 0:
            sign = 1
        else:
            sign = -1
        result += Decimal(sign) / (Decimal(2 * i + 1) * POW5[2 * i + 1])

    return result


def calc_pi():
    return Decimal(16) * arctg5(Decimal(1) / Decimal(5)) - Decimal(4) * arctg239(Decimal(1) / Decimal(239))

print calc_pi()
