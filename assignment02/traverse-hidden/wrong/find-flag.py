import requests
from tqdm import tqdm

INFIlE = "readmes-found.txt"
MATCH = "flag"
OUTFILE = "readmes-contents.txt"
OUTFILE_LONG = "readme-contents-long.txt"
USUAL_FILE_LENGTH = 69

with open(OUTFILE_LONG, "w") as out_file_long:
    with open(OUTFILE, "w") as out_file:
        num_lines = sum(1 for line in open(INFIlE, "r"))
        with open(INFIlE, "r") as in_file:
            for link in tqdm(in_file, total=num_lines):
                content = requests.get(link.rstrip()).text
                if MATCH in content.lower() or not content == content[0] * len(content):
                    # print(content)
                    pass
                out_file.write(content + "\n")
                if len(content) != USUAL_FILE_LENGTH:
                    out_file_long.write(f"LONG--{link.rstrip()}--{content}\n")
