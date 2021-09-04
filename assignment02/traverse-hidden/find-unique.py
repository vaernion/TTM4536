import requests
from tqdm import tqdm

INFIlE = "readmes-found.txt"
OUTFILE = "readmes-unique.txt"
unique = set()

with open(OUTFILE, "w") as out_file:
    num_lines = sum(1 for line in open(INFIlE, "r"))
    with open(INFIlE, "r") as in_file:
        for link in tqdm(in_file, total=num_lines):
            content = requests.get(link.rstrip()).text
            if content not in unique:
                unique.add(content)
                out_file.write(content)
