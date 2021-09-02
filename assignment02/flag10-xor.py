import os

HASHES="flag10-hashedpasswords-matches.txt"
ints = []
hexes = []

with open(os.path.join(os.path.dirname(__file__),HASHES)) as f:
    for index, line in enumerate(f):
        line_int = int(line.strip(),16)
        ints.append(line_int)
        hexes.append(hex(line_int))


xored = ints[0]

for i,x in enumerate(ints):
    if i == 0:
        # print(xored)
        # print(bin(xored))
        continue
    xored = xored ^ x
    # print(xored)
    # print(bin(xored))

print(xored)
print(hex(xored))
print("00"+str(hex(xored))[2:])
# 005c188994e3df2d51a1bf792042ed72d391c905c90e151587300c06fdf74cc9
