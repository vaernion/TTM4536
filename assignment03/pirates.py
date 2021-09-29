import glob
import os
import sys

import Crypto
import gmpy2
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from gmpy2 import mpz
from sympy import *

gmpy2.get_context().precision = 100000


def breakRSA():
    public_keys = glob.glob(os.path.join(os.path.dirname(__file__), "keys/*"))
    solutions = []
    for index, key_filename in enumerate(public_keys):
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
    SHIFT_MIN = mpz(nextprime(2 ** 1045 - 1))

    p_approx = gmpy2.iroot_rem((n) - (P_MIN * SHIFT_MIN), 3)[0]
    p = p_approx
    q = mpz(1)  # prevent UnboundLocalError during KeyboardInterrupt

    ERR_NOT_MATCH_MODULUS = "RSA factors do not match modulus"
    err_not_match_modulus_count = 0
    err_n_not_equal_count = 0
    err_not_implemented_count = 0
    err_p_not_in_n = 0
    i = 0

    while True:
        try:
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

            rem = gmpy2.t_mod(n, p)
            if rem != 0:
                err_p_not_in_n += 1
                continue

            # print(f"found P? {p=}")
            q = gmpy2.div(n, p)
            n2 = p * q
            # print(n2 == n, type(n2), type(n), type(p), type(q), mpfr.is_integer(q)) # verify valid values

            phi = mpz(p - 1) * mpz(q - 1)
            d = Crypto.Util.number.inverse(e, int(phi))
            rsa_components = (int(n), e, d, int(p), int(q))

            newkey = RSA.construct(rsa_components)
            cipher_rsa = PKCS1_OAEP.new(newkey)

            return (key_filename, cipher_rsa)

        except KeyboardInterrupt:
            print(
                f"\n\n{i=} {err_not_match_modulus_count=} {err_n_not_equal_count=} {err_not_implemented_count=} {err_p_not_in_n=}"
            )
            print(f"n-(p*q): {n-(p*q)}")
            sys.exit(1)
        except ValueError as err:
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
    binfiles = glob.glob(os.path.join(os.path.dirname(__file__), "bin/*"))
    for binfilename in binfiles:
        with open(binfilename, "rb") as file:
            try:
                encrypted_message = file.read()
                message = cipher_rsa[1].decrypt(encrypted_message)
                print(
                    f"--DECRYPTED FILE: {binfilename} ENCODED WITH: {cipher_rsa[0]}\n{message=}\n\n"
                )

            except (TypeError, ValueError) as err:
                print(err)
                continue


def main():
    solutions = breakRSA()
    for solution in solutions:
        readBins(solution["cipher"])


if __name__ == "__main__":
    main()
