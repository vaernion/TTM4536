INFILE = "readmes-found.txt"
OUTFILE = "readmes-found-sorted.txt"
urls = []


with open(INFILE, "r") as in_file:
    for link in in_file:
        link = link.rstrip()
        key = link[-5:]
        urls.append((key, link))

urls = sorted(urls, key=lambda e: e[0])
print(urls[0], urls[-1])

with open(OUTFILE, "w") as out_file:
    for url in urls:
        out_file.write(url[1] + "\n")
