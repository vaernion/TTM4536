# 2^grade mod p = flag3 mod 2^64
# where p = Next_Prime(2^64)

# from wolframalpha asking next prime after 2^64
NEXT_PRIME = 18446744073709551629
p = NEXT_PRIME  # Next_Prime(2^64)

flag3 = "24bea01a261043e2e5f504594e360ec5"
flag3int = int(flag3, 16)  # # 48841991508627492082512072253508030149
right_side = flag3int % (2 ** 64)  # 16570155185590374085

print(f"{right_side=} {p=}")

left_side = 0
n = 830_000  # update while progressing brute force
PROGRESS_EVERY = 10_000
i = 0

while left_side != right_side:
    if i % PROGRESS_EVERY == 0:
        print(f"{i=} {n=} {left_side=}")
    n += 1
    i += 1
    left_side = (2 ** n) % p

print(f"{left_side=}  {n=}")
