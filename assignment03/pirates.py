import os
import sys

import Crypto
import gmpy2
import mpmath
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from gmpy2 import mpc, mpfr, mpq, mpz
from mpmath import *
from sympy import *

mpc.prec = 100000


def genKeys():
    # stuff

    pp = []
    qq = []
    for i in range(4):
        p = randprime(2 ** 1023, 2 ** 1024 - 1)
        pp.append(p)
        shift = randprime(2 ** 1045, 2 ** 1046 - 1)
        q = nextprime(p * p + shift)
        qq.append(q)

    nn = []
    for i in range(4):
        nn.append(pp[i] * qq[i])

    tmpRSAkeys = []
    for i in range(4):
        newd = Crypto.Util.number.inverse(65537, (pp[i] - 1) * (qq[i] - 1))
        newkey = RSA.construct((nn[i], 65537, newd, pp[i], qq[i]))
        tmpRSAkeys.append(newkey)

    # more stuff


def main():
    a = 2 ** 1050
    print(a)


if __name__ == "__main__":
    main()
