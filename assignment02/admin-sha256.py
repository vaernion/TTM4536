import random
import string
from hashlib import sha256

CHARS = string.ascii_letters + "0123456789"
prefix = "gathorhe"
flag07rightmost = "daebda86"
SUFFIX_MAX_LENGTH = 2

unique = set()

print(CHARS)


def main():
    find_match()
    print("unique inputs:", len(unique))


def generate_suffix(length: int, seed: int):
    output = ""
    print(f"{length=} {seed=}")
    for n in range(1, length + 1):
        char = CHARS[int(seed / n) % len(CHARS)]
        # print(f"{char=}")
        output += char
    print(output)
    return output


def find_match():
    for postfix_length in range(1, SUFFIX_MAX_LENGTH + 1):
        for seed in range(len(CHARS) ** postfix_length):
            if seed != 77:
                continue
            suffix = generate_suffix(postfix_length, seed)
            # print(suffix)
            input = prefix + suffix
            unique.add(input)
            # print(input)

            h = sha256()
            x = h.update(bytes(input, "utf-8"))
            x = h.hexdigest()
            # print(x[-8:], flag07rightmost)
            if x[-8:] == flag07rightmost:
                print(f"MATCH: {x}")
                break


if __name__ == "__main__":
    main()
