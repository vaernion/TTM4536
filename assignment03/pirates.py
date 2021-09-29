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
gmpy2.get_context().precision = 100000
# print(gmpy2.get_context())


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
        # if index != 0:
        #     continue

        public_key = RSA.importKey(open(key_filename).read())
        n = public_key.n  # int ~3017 bits
        e = public_key.e  # int 65537

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
    n = mpz(n)
    USE_TEST = False

    ### sanity check during debugging
    # n_test = mpz(3233)
    # p_test = mpz(61)
    # q_test = n_test / p_test  # 53
    # n2_test = q_test * p_test
    # mod5 = n_test % p_test == 0
    # print(n_test, n2_test, p_test, q_test, mod5)
    # print(type(n_test), type(n2_test), n_test == n2_test, n_test % p_test == 0)

    #### SOLVED breaking randomly generated test value
    if USE_TEST:
        p_test = randprime(2 ** 1023, 2 ** 1024 - 1)
        shift_test = randprime(2 ** 1045, 2 ** 1046 - 1)
        q_test = nextprime(p_test * p_test + shift_test)
        newd_test = Crypto.Util.number.inverse(65537, (p_test - 1) * (q_test - 1))
        newkey_test = RSA.construct((p_test * q_test, 65537, newd_test, p_test, q_test))
        n_test = newkey_test.n
        e_test = newkey_test.e
        n = mpz(n_test)
        e = e_test
        print(f"{e_test=} {n_test=}")

    print(f"-- finding key {index=} {key_filename=}")
    P_MIN = mpz(nextprime(2 ** 1023 - 1))
    # P_MAX = mpz(nextprime(2 ** 1024 - 1))
    SHIFT_MIN = mpz(nextprime(2 ** 1045 - 1))
    # SHIFT_MAX = mpz(nextprime(2 ** 1046 - 1))
    # print(f"{mpfr(P_MIN)=}\n{mpfr(P_MAX)=}")

    # p_root = mpfr(n) ** (1 / 3)  # cube root
    # n_iroot_rem = gmpy2.iroot_rem(n, 3)
    # p_root = n_iroot_rem[0]
    # p_root_remainder = n_iroot_rem[1]

    # p_approx = p_root
    # p_approx = ((n) - (P_MIN * SHIFT_MIN)) ** (1 / 3)
    p_approx = gmpy2.iroot_rem((n) - (P_MIN * SHIFT_MIN), 3)[0]
    # p_approx = mpz(nextprime(p_approx))
    p = p_approx
    q = mpz(1)
    # print(f"{mpfr(p_approx)=}\n{p=}")

    ERR_NOT_MATCH_MODULUS = "RSA factors do not match modulus"
    err_not_match_modulus_count = 0
    err_n_not_equal_count = 0
    err_not_implemented_count = 0
    err_p_not_in_n = 0
    i = 0

    while True:
        try:
            # p = mpz(nextprime(p))
            p = mpz(prevprime(p))
            if USE_TEST:
                if i % 100 == 0:
                    print(
                        "p_test diff len",
                        len(str(p_test)) - len(str(p)),
                        "len p:",
                        len(str(p)),
                        "len p_test:",
                        len(str(p_test)),
                        "len diff:",
                        len(str(p_test - p)),
                    )
                    print("p_test diff:", p_test - p)
                if p == p_test:
                    q = gmpy2.div(n, p)
                    n2 = p * q
                    rem = gmpy2.t_mod(n, p)
                    print(
                        f"### found p test, {(p==p_test)=} {(q==q_test)=} {(n2==n_test)=} {(rem==0)=} ###"
                    )

            # q = mpz(n) / mpz(p)
            rem = gmpy2.t_mod(n, p)
            # rem = n % p
            if rem != 0:
                err_p_not_in_n += 1
                continue

            print(f"found P? {p=}")
            q = gmpy2.div(n, p)
            n2 = p * q
            print(n2 == n, type(n2), type(n), type(p), type(q), mpfr.is_integer(q))
            # while (n2) != n:
            #     if n2 < n:
            #         q = mpz(nextprime(q))
            #     else:
            #         q = mpz(prevprime(q))
            #     n2 = p * q
            #     print("diff:", n - (p * q))
            #     # print(type(n), type(p), type(q))
            # print("escaped loop")

            # if not mpfr.is_integer(q):
            #     raise Exception("Q division error")
            # print(type(p), type(q))
            # n2 = mpz(p * q)
            # if n != n2:
            #     err_n_not_equal_count += 1
            #     # print(mpz(n), mpz(n2))
            #     # print("\n\nn1:", n)
            #     # print("n2", n2, type(int(n2)), type(n), "equal:", n == int(n2))
            #     # print("n2", n2, "\n\n")
            #     print("minus",n2 - n)
            #     continue

            phi = mpz(p - 1) * mpz(q - 1)
            # d = gmpy2.invert(mpz(e), phi)
            d = Crypto.Util.number.inverse(e, int(phi))
            rsa_components = (int(n), e, d, int(p), int(q))
            # print(type(n), type(e), type(d), type(p), type(q))
            # print([type(x) for x in rsa_components])

            newkey = RSA.construct(rsa_components)
            cipher_rsa = PKCS1_OAEP.new(newkey)
            print("newkey", newkey)
            print("cipher_rsa", cipher_rsa)

            # readBins(cipher_rsa)
            return cipher_rsa

        except KeyboardInterrupt:
            print(
                f"\n\n{i=} {err_not_match_modulus_count=} {err_n_not_equal_count=} {err_not_implemented_count=} {err_p_not_in_n=}"
            )
            # print(f"{p-p_approx =}")
            print(f"n-(p*q): {n-(p*q)}")
            sys.exit(1)
        except ValueError as err:
            # print("findKey() ValueError:", err)
            if str(err) == ERR_NOT_MATCH_MODULUS:
                err_not_match_modulus_count += 1
                continue
            raise err
        except NotImplementedError:
            # invert threw
            err_not_implemented_count += 1
            continue
        finally:
            i += 1


def readBins(cipher_rsa):
    print("readBins", cipher_rsa)

    binfiles = glob.glob(os.path.join(os.path.dirname(__file__), "bin/*"))
    for binfilename in binfiles:
        with open(binfilename, "rb") as file:
            try:
                # print(binfilename)
                encrypted_message = file.read()

                # print(cipher_rsa)
                message = cipher_rsa.decrypt(encrypted_message)
                print(f"--FILE: {binfilename}\n{message=}\n\n")
            except TypeError as err:
                print(err)
            except ValueError as err:
                print(err)
                continue


def main():
    solutions = breakRSA()
    print(f"{solutions=}")
    for solution in solutions:
        readBins(solution["cipher"])


if __name__ == "__main__":
    main()
