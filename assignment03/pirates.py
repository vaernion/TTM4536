import glob
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

mp.prec = 100000


# def genKeys():
#     # stuff

#     pp = []
#     qq = []
#     for i in range(4):
#         p = randprime(2 ** 1023, 2 ** 1024 - 1)
#         pp.append(p)
#         shift = randprime(2 ** 1045, 2 ** 1046 - 1)
#         q = nextprime(p * p + shift)
#         qq.append(q)

#     nn = []
#     for i in range(4):
#         nn.append(pp[i] * qq[i])

#     tmpRSAkeys = []
#     for i in range(4):
#         newd = Crypto.Util.number.inverse(65537, (pp[i] - 1) * (qq[i] - 1))
#         newkey = RSA.construct((nn[i], 65537, newd, pp[i], qq[i]))
#         tmpRSAkeys.append(newkey)

#     # more stuff


def breakRSA():
    public_keys = glob.glob(os.path.join(os.path.dirname(__file__), "keys/*"))
    solutions = []
    for index, key_filename in enumerate(public_keys):
        if index != 3:
            continue  # only work on first key for now

        public_key = RSA.importKey(open(key_filename).read())
        n = public_key.n  # int ~3017 bits
        e = public_key.e  # int 65537

        # print(f"{e=}\n{n=}")
        try:
            newkey = findKey(n, e, index, key_filename)
            solution = {
                "filename": key_filename,
                "public": public_key,
                "cipher": newkey,
            }
            solutions.append(solution)
        except ValueError as e:
            print("breakRSA Error:", e)
            continue
    return solutions


def findKey(n, e, index, key_filename):
    print(f"-- finding key {index=} {key_filename=}")
    P_MAX = mpz(nextprime(2 ** 1024))
    P_MIN = mpz(nextprime(2 ** 1023) - 1)
    SHIFT_MIN = mpz(nextprime(2 ** 1045))
    SHIFT_MAX = mpz(nextprime(2 ** 1046) - 1)
    print(f"{mpfr(P_MIN)=}\n{mpfr(P_MAX)=}")

    # p_root = mpz(n) ** (1 / 3)  # cube root
    n_iroot_rem = gmpy2.iroot_rem(n, 3)
    p_root = n_iroot_rem[0]
    p_root_remainder = n_iroot_rem[1]

    p_approx = (mpz(n) - (p_root * SHIFT_MIN)) ** mpfr(1 / 3)
    p_approx = mpz(nextprime(p_approx))
    # p = P_MIN
    p = p_approx
    print(f"{mpfr(p_approx)=}\n{p=}")

    i = 0
    ERR_NOT_MATCH_MODULUS = "RSA factors do not match modulus"
    err_not_match_modulus_count = 0

    while p < P_MAX:
        # while p > P_MIN:
        try:
            p = nextprime(p, 1)
            # p = prevprime(p)
            q = mpz(n) / mpz(p)
            # print("q:", type(q), "p:", type(p))
            if not mpfr.is_integer(q):
                raise Exception("Q division error")

            phi = mpz((p - 1)) * mpz((q - 1))
            # d = gmpy2.invert(mpz(e), phi)
            d = Crypto.Util.number.inverse(e, int(phi))
            rsa_components = (n, e, d, p, int(q))
            # print(type(n), type(e), type(d), type(p), type(q))
            # print([type(x) for x in rsa_components])

            newkey = RSA.construct(rsa_components)
            cipher_rsa = PKCS1_OAEP.new(newkey)
            print("newkey", newkey)
            print("cipher_rsa", cipher_rsa)
            return cipher_rsa

        except KeyboardInterrupt:
            print(
                f"\n{i=} {err_not_match_modulus_count=}\ncurrent p:{mpfr(p)=}\n{mpz(p)=}"
            )
            print(f"{p-p_approx =}")
            sys.exit(1)
        except ValueError as err:
            # print("findKey() ValueError:", err)
            if str(err) == ERR_NOT_MATCH_MODULUS:
                err_not_match_modulus_count += 1
            continue
        except NotImplementedError:
            # invert threw
            continue

        finally:
            i += 1

    print(f"iterations: {i=}")
    raise Exception("no key found")


def readBins(cipher_rsa):
    print("readBins", cipher_rsa)

    binfiles = glob.glob(os.path.join(os.path.dirname(__file__), "bin/*"))
    for file in binfiles:
        with open(file, "rb") as encrypted_message:
            try:
                message = cipher_rsa.decrypt(encrypted_message)
                print(message)
            except TypeError as err:
                print(err)


def main():
    solutions = breakRSA()
    for solution in solutions:
        readBins(solution["cipher"])


if __name__ == "__main__":
    main()
