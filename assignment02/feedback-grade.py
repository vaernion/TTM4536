# 2^grade mod p = flag3 mod 2^64
# where p = Next_Prime(2^64)

# from wolframalpha asking next prime after 2^64
NEXT_PRIME = 18446744073709551629


# def is_prime(x):
#     return all(x % i for i in range(2, x))
# def next_prime(x):
#     return min([a for a in range(x + 1, 2 * x) if is_prime(a)])
# print(next_prime(2 ** 64))

grade = 0  # unknown, goal to find
grade_base = 2

p = NEXT_PRIME  # Next_Prime(2^64)
flag3 = 0
flag3int = int(flag3, 16)  # unknown, needed to solve - convert hex to dec?
right_side = flag3int % (2 ** 64)

print(right_side)
