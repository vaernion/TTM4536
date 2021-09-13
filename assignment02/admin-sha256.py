import itertools
import string
from hashlib import sha256

# CHARS = string.ascii_letters + string.digits
CHARS = string.ascii_letters + string.digits + string.punctuation
# CHARS = string.hexdigits
# CHARS = string.ascii_lowercase
PREFIX = "gathorhe"
FLAG7LAST8 = "daebda86"
SUFFIX_MIN_LENGTH = 4
SUFFIX_MAX_LENGTH = 8

print(len(CHARS), CHARS[0], CHARS[-1])
print("." in CHARS)
for char in CHARS:
    print(char)


print(len("a"))
print(len(string.punctuation))


def main():
    match = find_match()
    if match is not None:
        print(f"MATCH: sha256({match[0]}) == {match[1]}")
    else:
        print("no match found")


def find_match():
    for postfix_length in range(SUFFIX_MIN_LENGTH, SUFFIX_MAX_LENGTH + 1):
        for perm in itertools.permutations(CHARS, postfix_length):
            suffix = "".join(perm)
            password = PREFIX + suffix

            h = sha256()
            h.update(bytes(password, "utf-8"))
            hash = h.hexdigest()
            # print(f"{password=} {hash=} x[-8:]={hash[-8:]}")

            if hash[-8:] == FLAG7LAST8:
                return (password, hash)
    return None


if __name__ == "__main__":
    main()
