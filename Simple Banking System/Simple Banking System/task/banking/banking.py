import random
import sqlite3


class BankCard:
    def __init__(self):
        self.bool = True
        self.data = sqlite3.connect("card.s3db")
        self.db = self.data.cursor()
        self.CreateDatabase()
        self.Ask()

    def Ask(self):
        while self.bool:
            print("1. Create an account")
            print("2. Log into account")
            print("3. Exit")
            choice = input()
            print("")

            if choice == "1":
                self.CreateCard()
            elif choice == "2":
                self.LogIn()
            else:
                print("Bye!")
                break

    def CreateCard(self):
        pin = str(random.randint(0, 10000)).rjust(4, "0")
        card_number = self.LuhnAlgorithm("400000" + str(random.randint(0, 1000000000)).rjust(9, "0"))
        self.AddDatabase(card_number, pin)
        print("Your card has been created")
        print(f"Your card number:\n{card_number}")
        print(f"Your card PIN:\n{pin}")
        print("")

    def LogIn(self):
        print("Enter your card number:")
        c_num = input()
        print("Enter your PIN:")
        p = input()
        print("")
        data = self.Check(c_num, p)
        print("Wrong card number or PIN!") if not data else self.Account(data)

    def AddIncome(self, data):
        print("\nEnter income:")
        income = int(input())
        self.db.execute(f"UPDATE card SET balance = balance + {income} WHERE id = {data[0]};")
        self.data.commit()
        print("Income was added!")

    def DoTransfer(self, data):
        print("\nTransfer")
        print("Enter card number:")
        card_number = input()

        if card_number == data[0]:
            print("You can't transfer money to the same account!")
            return

        if self.LuhnAlgorithm(card_number[:-1]) != card_number:
            print("Probably you made mistake in the card number. Please try again!")
            return

        banker = self.db.execute(f"SELECT * FROM card WHERE number = {card_number};")
        self.data.commit()

        other = banker.fetchone()

        if not other:
            print("Such a card does not exist.")
            return

        print("Enter how much money you want to transfer:")
        money = int(input())

        print(data[3])

        if money > data[3]:
            print("Not enough money!")
            return

        self.db.execute(f"UPDATE card SET balance = balance + {money} WHERE id = {other[0]};")
        self.data.commit()

        self.db.execute(f"UPDATE card SET balance = balance - {money} WHERE id = {data[0]};")
        self.data.commit()

        print("Success!")

    def CloseAccount(self, data):
        self.db.execute(f"DELETE FROM card WHERE id = {data[0]};")
        self.data.commit()
        print("The account has been closed!")

    def Account(self, data):
        print("You have successfully logged in!")

        while True:
            print("\n1. Balance")
            print("2. Add income")
            print("3. Do transfer")
            print("4. Close account")
            print("5. Log out")
            print("0. Exit")
            c = input()

            if c == "1":
                print(f"Balance: {data[3]}")
            elif c == "2":
                self.AddIncome(data)
            elif c == "3":
                self.DoTransfer(data)
            elif c == "4":
                self.CloseAccount(data)
                break
            elif c == "5":
                print("You have successfully logged out!")
                break
            else:
                self.bool = False
                break

            data = self.Check(data[1], data[2])

    def LuhnAlgorithm(self, card_number):
        def Check(x):
            return x - 9 if x > 9 else x

        checksum = list(map(int, list(card_number)))
        luhn = []

        for i in range(len(checksum)):
            if (i + 1) % 2 == 1:
                luhn.append(checksum[i] * 2)
            else:
                luhn.append(checksum[i])

        luhn = list(map(Check, luhn))
        checksum.append(0 if sum(luhn) % 10 == 0 else (sum(luhn) // 10 + 1) * 10 - sum(luhn))

        return "".join(map(str, checksum))

    def CreateDatabase(self):
        self.db.execute("""CREATE TABLE IF NOT EXISTS card(
        id INTEGER NOT NULL,
        number TEXT,
        pin TEXT,
        balance INTEGER DEFAULT 0);""")

        self.data.commit()

    def AddDatabase(self, card_number, pin, balance=0):
        self.db.execute(f"""INSERT INTO card (id, number, pin, balance) 
        VALUES ({random.randint(0, 1000000000)}, {card_number}, {pin}, {balance});""")
        self.data.commit()

    def Check(self, card_number, pin):
        banker = self.db.execute(f"""SELECT * FROM card
        WHERE number = {card_number} AND pin = {pin};""")
        self.data.commit()

        return banker.fetchone()


card = BankCard()
