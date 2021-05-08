import requests
from bs4 import BeautifulSoup
import subprocess
import re
from urllib.parse import urlsplit

from config import DOWNLOAD_FOLDER, IDM_PATH


class Base:
    def get_page_html(self, url: str) -> str:
        resp = requests.get(url)
        return resp.text

    def html_parser(self, url: str, schema: str, parser: str = 'lxml'):
        html = self.get_page_html(schema + url)
        return BeautifulSoup(html, parser)

    def command_parser(self, commands: list) -> None:
        commands.insert(0, self.idm_path)
        print(commands[4], ": ", commands[2])
        result = subprocess.run(commands, capture_output=True, text=True)
        if result.stdout:
            print("stdout: ", result.stdout)
        if result.stderr:
            print("stderr: ", result.stderr)


class Scraper(Base):
    def __init__(self, schema: str = "https://panel.bitso.ir", to_iran: bool = True) -> None:
        self.download_direcotry = DOWNLOAD_FOLDER
        self.idm_path = IDM_PATH
        self.new_sv = "ir"
        self.schema = schema
        self.to_iran = to_iran

    def download(self, directory_url: str):
        parser = self.html_parser(directory_url, self.schema)
        title = self.get_page_title(parser)
        files = self.get_files(parser)
        directories = self.get_directories(parser)
        self.process_files(files, self.download_direcotry + title)
        for _, url in directories.items():
            self.download(url)

    def get_files(self, parser: BeautifulSoup):
        links = {link.text: link['href'] for link in parser.find('div', class_='file-list').find_all('a')}
        return {link: links.get(link) for link in links if '/dnl/' in links.get(link)}
    
    def get_directories(self, parser: BeautifulSoup):
        links = {link.text: link['href'] for link in parser.find('div', class_='file-list').find_all('a')}
        return {link: links.get(link) for link in links if '/dnl/' not in links.get(link)}

    def process_files(self, files: dict, directory: str):
        for filename, url in files.items():
            self.add_to_queue(url=url, filename=filename, local_path=directory)

    def get_page_title(self, parser: BeautifulSoup):
        path_list = parser.find('h3', class_='panel-heading').find('title').find_all('li')
        path_list = [title.text.strip() for title in path_list]
        return "\\".join(path_list)
    
    def to_iran_server(self, url: str, new_sv: str):
        old_sv = url.replace("https://", "").split(".bitso")[0]
        sv = re.findall(r'\d+', old_sv)
        sv = "".join(sv)
        url = url.replace(old_sv, new_sv).replace("https", "http")
        return f"{url}?s={sv}"

    def add_to_queue(self, url: str, filename: str, start: bool = False, local_path: str = None) -> None:
        commands = []
        if self.to_iran:
            url = self.to_iran_server(url, self.new_sv)
        commands.append('/d')
        commands.append(url)
        commands.append('/f')
        commands.append(filename)
        if start:
            commands.append('/s')
        if local_path:
            commands.append('/p')
            commands.append(local_path)
        commands.append('/a')

        self.command_parser(commands)


def auto_add_queue(url: str):
    base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
    scraper = Scraper(to_iran=True)
    scraper.download(url.replace(base_url, "/"))