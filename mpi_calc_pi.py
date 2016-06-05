# coding: utf-8
from decimal import Decimal, getcontext

from mpi4py import MPI

PRECISION = 50  # Podzielne przez liczbe procesów
getcontext().prec = PRECISION
POW239 = [Decimal(1)]
POW5 = [Decimal(1)]

CALC_TAG = 11

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.Get_size()


def initialize_powers():
    """
        Precomputing for calculating powers.
        Caching powers.
    """
    for i in xrange(1, PRECISION * 2 + 1):
        POW239.append(POW239[i - 1] * Decimal(239))
        POW5.append(POW5[i - 1] * Decimal(5))


def arctg239(lower_bound, higher_bound):
    """
        Szereg Talora dla arctg 239.
    """
    result = Decimal(0)
    for i in xrange(lower_bound, higher_bound):
        if i % 2 == 0:
            sign = 1
        else:
            sign = -1
        result += Decimal(sign) / (Decimal(2 * i + 1) * POW239[2 * i + 1])

    return result


def arctg5(lower_bound, higher_bound):
    """
        Szereg Taylora dla arctg 5.
        Możliwa niedokładność dla dwóch ostatnich liczb.
    """
    result = Decimal(0)
    for i in xrange(lower_bound, higher_bound):
        if i % 2 == 0:
            sign = 1
        else:
            sign = -1

        result += Decimal(sign) / (Decimal(2 * i + 1) * POW5[2 * i + 1])
    return result


def calc_pi():
    initialize_powers()
    lower_bound = (rank) * (PRECISION / (size))
    higher_bound = (
        (rank) * (PRECISION / (size)) +
        (PRECISION / (size))
    )

    if rank == 0:
        result = {
            '5': arctg5(lower_bound, higher_bound),
            '239': arctg239(lower_bound, higher_bound)
        }
        for task_no in xrange(1, size):
            partial = comm.recv()
            result['5'] += partial['5']
            result['239'] += partial['239']

        print (Decimal(16) * result['5'] - Decimal(4) * result['239'])

    else:
        arc_5 = arctg5(lower_bound, higher_bound)
        arc_239 = arctg239(lower_bound, higher_bound)
        result = {
            '5': arc_5, '239': arc_239
        }
        comm.send(result, dest=0, tag=CALC_TAG)


calc_pi()
