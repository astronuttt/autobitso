import requests
import re
import sys


new_sv = 'ir'


def get_urls(url: str) -> list:
    res = requests.get(url).text
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

    ur = re.findall(regex, res)

    urls = [u[0] for u in ur]
    return urls


def replace_domain(url: str) -> str:
    old_sv = url.replace("https://", "").split(".bitso")[0]
    sv = re.findall(r'\d+', old_sv)
    sv = "".join(sv)
    url = url.replace(old_sv, new_sv).replace("https", "http")
    return f"{url}?s={sv}"


def print_from_url(url: str):
    urls = get_urls(url)
    for link in urls:
        print(replace_domain(link))


def write_from_url(url: str, filename: str):
    urls = get_urls(url)
    new_urls = []

    with open(filename, "w") as f:
        for link in urls:
            new_urls.append(replace_domain(link) + "\n")
        f.writelines(new_urls)
    print(f"Done!\twritten urls: {len(new_urls)}\t org urls: {len(urls)}")


def edit_file_urls(filename: str):
    new_urls = []
    with open(filename, 'r') as f:
        urls = f.readlines()

    with open(filename, 'w') as f:
        for link in urls:
            new_urls.append(replace_domain(link.rstrip()) + "\n")
        f.writelines(new_urls)
    print(f"Done!\twritten urls: {len(new_urls)}\t org urls: {len(urls)}")

