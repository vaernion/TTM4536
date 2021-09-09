from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

HOST = "129.241.200.165"
PORT = 30606
PATH = ".hidden/"
UP_LINK_LENGTH = 3
README_LINK_LENGTH = 11
SUBFOLDER_LINK_LENGTH = 27
BASE_URL = urljoin(f"http://{HOST}:{PORT}", PATH)
print(BASE_URL)

OUTFILE_READMES = "readmes-found.txt"
OUTFILE_OTHER = "other-found.txt"


def main():
    req = requests.get(BASE_URL)
    soup = BeautifulSoup(req.content, "html.parser")

    links = find_links(soup)

    with tqdm(total=(26 ** 3 + 26 ** 2 + 26)) as pbar:
        readme_links, other_links = traverse(links, BASE_URL, pbar)
        print(f"readmes: {len(readme_links)}")
        print(f"interesting: {len(other_links)}")
        with open(OUTFILE_READMES, "w") as f:
            for link in readme_links:
                f.write(link + "\n")
        with open(OUTFILE_OTHER, "w") as f:
            for link in other_links:
                f.write(link + "\n")


def find_links(el):
    return list(map(lambda link: link.get("href"), el.find_all("a")))


def traverse(links: list, path: str, pbar):
    results = [[], []]
    for link in links:
        if link.startswith("README"):
            results[0].append(urljoin(path, link))
            pbar.update()
        # something interesting
        elif (
            not (link.startswith("..") and len(link) == UP_LINK_LENGTH)
            and len(link) != SUBFOLDER_LINK_LENGTH
        ):
            print(f"found something strange: {link}")
            results[1].append(urljoin(path, link))
            pbar.update()
        # traverse deeper
        elif not link.startswith(".."):
            subpath = urljoin(path, link)
            subreq = requests.get(subpath)
            subsoup = BeautifulSoup(subreq.content, "html.parser")
            sublinks = find_links(subsoup)

            traversed = traverse(sublinks, subpath, pbar)
            results[0] += traversed[0]
            results[1] += traversed[1]
    return results


if __name__ == "__main__":
    main()
