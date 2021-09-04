import requests
from tqdm import tqdm

INFIlE = "readmes-found.txt"
OUTFILE = "readmes-unique-chars.txt"
unique = set()

with open(OUTFILE, "w") as out_file:
    num_lines = sum(1 for line in open(INFIlE, "r"))
    with open(INFIlE, "r") as in_file:
        for link in tqdm(in_file, total=num_lines):
            content = requests.get(link.rstrip()).text
            for char in content:
                if char not in unique:
                    unique.add(char)
                    out_file.write(char)
