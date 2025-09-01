import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class Client:
    def __init__(self, address):
        self.address = address
        self.accounts = []
        self.active = True

    def perform_transaction(self, account, transaction):
        if not self.active:
            print("\n@@@ Operation failed! This client is deactivated. @@@")
            return
        transaction.register(account)

    def add_account(self, account):
        self.accounts.append(account)


class Individual(Client):
    def __init__(self, name, birth_date, cpf, address):
        super().__init__(address)
        self.name = name
        self.birth_date = birth_date
        self.cpf = cpf


class Account:
    def __init__(self, number, client):
        self._balance = 0
        self._number = number
        self._branch = "0001"
        self._client = client
        self._history = History()

    @classmethod
    def new_account(cls, client, number):
        return cls(number, client)

    @property
    def balance(self):
        return self._balance

    @property
    def number(self):
        return self._number

    @property
    def branch(self):
        return self._branch

    @property
    def client(self):
        return self._client

    @property
    def history(self):
        return self._history

    def withdraw(self, amount):
        exceeded_balance = amount > self.balance

        if exceeded_balance:
            print("\n@@@ Operation failed! Insufficient funds. @@@")

        elif amount > 0:
            self._balance -= amount
            print("\n=== Withdrawal successful! ===")
            return True

        else:
            print("\n@@@ Operation failed! Invalid amount. @@@")

        return False

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print("\n=== Deposit successful! ===")
        else:
            print("\n@@@ Operation failed! Invalid amount. @@@")
            return False

        return True


class CheckingAccount(Account):
    def __init__(self, number, client, limit=500, withdraw_limit=3):
        super().__init__(number, client)
        self._limit = limit
        self._withdraw_limit = withdraw_limit

    def withdraw(self, amount):
        withdraws = len(
            [t for t in self.history.transactions if t["type"] == Withdrawal.__name__]
        )

        exceeded_limit = amount > self._limit
        exceeded_withdraws = withdraws >= self._withdraw_limit

        if exceeded_limit:
            print("\n@@@ Operation failed! Withdrawal amount exceeds limit. @@@")

        elif exceeded_withdraws:
            print("\n@@@ Operation failed! Maximum withdrawals exceeded. @@@")

        else:
            return super().withdraw(amount)

        return False

    def __str__(self):
        return f"""\
            Branch:\t\t{self.branch}
            Account:\t{self.number}
            Holder:\t\t{self.client.name}
        """


class SavingsAccount(Account):
    def __str__(self):
        return f"""\
            Branch:\t\t{self.branch}
            Savings:\t{self.number}
            Holder:\t\t{self.client.name}
        """


class History:
    def __init__(self):
        self._transactions = []

    @property
    def transactions(self):
        return self._transactions

    def add_transaction(self, transaction):
        self._transactions.append(
            {
                "type": transaction.__class__.__name__,
                "value": transaction.value,
                "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transaction(ABC):
    @property
    @abstractproperty
    def value(self):
        pass

    @abstractclassmethod
    def register(self, account):
        pass


class Withdrawal(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def register(self, account):
        success = account.withdraw(self.value)

        if success:
            account.history.add_transaction(self)


class Deposit(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def register(self, account):
        success = account.deposit(self.value)

        if success:
            account.history.add_transaction(self)


def menu():
    menu = """\n
    ================ MENU ================
    [1]\tDeposit
    [2]\tWithdraw
    [3]\tStatement
    [4]\tNew Checking Account
    [5]\tNew Savings Account
    [6]\tList Accounts
    [7]\tNew User
    [8]\tList Users
    [9]\tDeactivate User
    [0]\tExit
    => """
    return input(textwrap.dedent(menu))


def filter_client(cpf, clients):
    clients_filtered = [c for c in clients if c.cpf == cpf]
    return clients_filtered[0] if clients_filtered else None


def get_client_account(client):
    if not client.accounts:
        print("\n@@@ Client has no account! @@@")
        return
    return client.accounts[0]  # FIXME: allow choosing account


def deposit(clients):
    cpf = input("Enter client's CPF: ")
    client = filter_client(cpf, clients)

    if not client or not client.active:
        print("\n@@@ Client not found or inactive! @@@")
        return

    value = float(input("Enter deposit amount: "))
    transaction = Deposit(value)

    account = get_client_account(client)
    if not account:
        return

    client.perform_transaction(account, transaction)


def withdraw(clients):
    cpf = input("Enter client's CPF: ")
    client = filter_client(cpf, clients)

    if not client or not client.active:
        print("\n@@@ Client not found or inactive! @@@")
        return

    value = float(input("Enter withdrawal amount: "))
    transaction = Withdrawal(value)

    account = get_client_account(client)
    if not account:
        return

    client.perform_transaction(account, transaction)


def show_statement(clients):
    cpf = input("Enter client's CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\n@@@ Client not found! @@@")
        return

    account = get_client_account(client)
    if not account:
        return

    print("\n================ STATEMENT ================")
    transactions = account.history.transactions

    statement = ""
    if not transactions:
        statement = "No transactions found."
    else:
        for t in transactions:
            statement += f"\n{t['type']}:\n\tR$ {t['value']:.2f}"

    print(statement)
    print(f"\nBalance:\n\tR$ {account.balance:.2f}")
    print("===========================================")


def create_client(clients):
    cpf = input("Enter CPF (numbers only): ")
    client = filter_client(cpf, clients)

    if client:
        print("\n@@@ A client with this CPF already exists! @@@")
        return

    name = input("Enter full name: ")
    birth_date = input("Enter birth date (dd-mm-yyyy): ")
    address = input("Enter address (street, number - district - city/state): ")

    client = Individual(name=name, birth_date=birth_date, cpf=cpf, address=address)
    clients.append(client)

    print("\n=== Client created successfully! ===")


def create_account(account_number, clients, accounts, account_type="checking"):
    cpf = input("Enter client CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\n@@@ Client not found, account creation aborted! @@@")
        return

    if account_type == "checking":
        account = CheckingAccount.new_account(client=client, number=account_number)
    else:
        account = SavingsAccount.new_account(client=client, number=account_number)

    accounts.append(account)
    client.accounts.append(account)

    print("\n=== Account created successfully! ===")


def list_accounts(accounts):
    for account in accounts:
        print("=" * 100)
        print(textwrap.dedent(str(account)))


def list_users(clients):
    if not clients:
        print("\n@@@ No users found! @@@")
        return
    for client in clients:
        status = "Active" if client.active else "Inactive"
        print("=" * 100)
        print(f"Name:\t{client.name}")
        print(f"CPF:\t{client.cpf}")
        print(f"Birth Date:\t{client.birth_date}")
        print(f"Address:\t{client.address}")
        print(f"Status:\t{status}")


def deactivate_user(clients):
    cpf = input("Enter CPF of user to deactivate: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\n@@@ Client not found! @@@")
        return

    client.active = False
    print("\n=== User deactivated successfully! ===")


def main():
    clients = []
    accounts = []

    while True:
        option = menu()

        if option == "1":
            deposit(clients)

        elif option == "2":
            withdraw(clients)

        elif option == "3":
            show_statement(clients)

        elif option == "4":
            account_number = len(accounts) + 1
            create_account(account_number, clients, accounts, "checking")

        elif option == "5":
            account_number = len(accounts) + 1
            create_account(account_number, clients, accounts, "savings")

        elif option == "6":
            list_accounts(accounts)

        elif option == "7":
            create_client(clients)

        elif option == "8":
            list_users(clients)

        elif option == "9":
            deactivate_user(clients)

        elif option == "0":
            print("Exiting system. Thank you!")
            break

        else:
            print("\n@@@ Invalid option, please try again. @@@")


main()
