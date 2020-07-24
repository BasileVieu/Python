import sys
import os
import requests
from bs4 import BeautifulSoup
import colorama
from colorama import Fore


class Browser:
    commands = {"exit", "back"}
    tags = {"p": Fore.WHITE,
            'h1': Fore.WHITE,
            'h2': Fore.WHITE,
            'h3': Fore.WHITE,
            'h4': Fore.WHITE,
            'h5': Fore.WHITE,
            'h6': Fore.WHITE,
            'a': Fore.BLUE,
            'ul': Fore.WHITE,
            'ol': Fore.WHITE,
            'li': Fore.WHITE}

    def __init__(self):
        self.history = list()
        self.is_run = True
        self.files = set()
        self.path_to_file = "" if len(sys.argv) != 2 else sys.argv[1]
        colorama.init()
        self.Run()

    def CreateDir(self, dir_name):
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

    def DoCommand(self, command):
        if command == "exit":
            self.is_run = False
        elif command == "back":
            if len(self.history) > 1:
                self.history.pop()
                data = self.ReadDataFromFile(self.history[-1])
                print(data)

    def CheckUrl(self, site: str):
        url = site if site.startswith("https://") else "https://" + site
        return url

    def GetDataByUrl(self, url):
        url = self.CheckUrl(url)
        req = requests.get(url)
        req.encoding = 'utf-8'
        return req.text

    def ReadDataFromFile(self, file_name):
        path = self.path_to_file + "/" + file_name + ".txt"
        data = open(path, "r").read()
        return data

    def CleanHtmlData(self, html_data):
        soup = BeautifulSoup(html_data, "html.parser")
        clean_data = "\n".join(
            [Browser.tags[tag] + line.get_text().strip() for tag in Browser.tags for line in soup.find_all(tag)]
        )
        return clean_data

    def WriteDataInFile(self, site, data):
        self.CreateDir(self.path_to_file)
        file_name = ".".join(site.split(".")[:-1])

        self.history.append(file_name)
        self.files.add(file_name)

        file_path = self.path_to_file + "/" + file_name + ".txt"
        with open(file_path, "w") as file:
            file.write(data)

    def Run(self):
        while self.is_run:
            site = input()

            if site in Browser.commands:
                self.DoCommand(site)
                continue

            if site not in self.files and "." not in site:
                print("Error: Incorrect URL\n")
                continue

            if site in self.files:
                print(self.ReadDataFromFile(site))
                continue

            url_data = self.GetDataByUrl(site)
            data = self.CleanHtmlData(url_data)
            print(data)

            if len(sys.argv) == 2 and site not in self.files:
                self.WriteDataInFile(site, data)


if __name__ == "__main__":
    browser = Browser()
