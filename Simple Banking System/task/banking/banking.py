from random import randint
import sqlite3


class DataWork:
    CONN = sqlite3.connect('card.s3db')
    CURSOR = CONN.cursor()

    def save_change(self):
        pass

    def create_base(self):
        self.CURSOR.executescript("""CREATE TABLE IF NOT EXISTS card
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, pin TEXT,
                           balance INTEGER DEFAULT 0)
                       """)
        self.CONN.commit()

    def save_card(self, card):
        params = (card.number, card.pin, card.balance)
        self.CURSOR.execute("INSERT INTO card VALUES (NULL, ?, ?, ?)", params)
        self.CONN.commit()


class Card:
    def __init__(self, number, pin, balance):
        self.number = number
        self.pin = pin
        self.balance = balance


class Bank:
    def __init__(self):
        self.list_menu = {1: "Create an account", 2: "Log into account", 0: "Exit"}
        self.account_menu = {1: "Balance", 2: "Log out", 0: "Exit"}
        self.list_accounts = {}
        self.dt = DataWork()

    def menu(self):
        for k, v in self.list_menu.items():
            print(f"{k}) {v}")
        print()

    def acc_menu(self):
        for k, v in self.account_menu.items():
            print(f"{k}) {v}")
        print()

    def pin(self):
        return ''.join(str(randint(0, 9)) for _ in range(4))

    def luhn(self, card_number):
        odds = sum([int(x) * 2 if int(x) * 2 < 9 else int(x) * 2 - 9
                    for x in card_number[-1::-2]])
        evens = sum([int(x) for x in card_number[-2::-2]])
        crc = (evens + odds) % 10
        if crc == 0:
            return "0"

        return str(10 - crc)

    def account(self):
        card_number = "400000" + ''.join(str(randint(0, 9)) for _ in range(9))
        return card_number + self.luhn(card_number)

    def create_account(self):
        pin = self.pin()
        account = self.account()
        card = Card(account, pin, 0)
        return card

    def login(self):
        print("Enter your card number:")
        number = input()
        print("Enter your PIN:")
        pin = input()
        print()
        if number in self.list_accounts and \
                self.list_accounts[number].pin == pin:
            return self.list_accounts.get(number)

        return None

    def run(self):
        self.dt.create_base()
        while True:
            self.menu()
            choose = input()
            if choose == "1":
                card = self.create_account()
                print("Your card has been created")
                print("Your card number:")
                print(card.number)
                print("Your card PIN:")
                print(card.pin)
                self.list_accounts[card.number] = card
                self.dt.save_card(card)
                print()
            elif choose == "2":
                card = self.login()
                if card is not None:
                    print("You have successfully logged in!")
                    print()
                    while True:
                        self.acc_menu()
                        choose = input()
                        if choose == "1":
                            print(f"Balance: {card.balance}")
                            print()
                        elif choose == "2":
                            print("You have successfully logged out!")
                            print()
                            break
                        elif choose == "0":
                            quit()
                else:
                    print("Wrong card number or PIN!")
                    print()
            elif choose == "0":
                print("Bye!")
                quit()


# dt = DataWork()

b = Bank()
b.run()
