import textwrap
from abc import ABC, abstractmethod
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
        self._balance = 0.0
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

    # Savings and base account: no overdraft allowed here
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
            return True
        else:
            print("\n@@@ Operation failed! Invalid amount. @@@")
            return False


class CheckingAccount(Account):
    def __init__(self, number, client, per_tx_limit=500.0, withdraw_limit=3, overdraft_limit=300.0):
        super().__init__(number, client)
        self._per_tx_limit = per_tx_limit
        self._withdraw_limit = withdraw_limit
        self._overdraft_limit = overdraft_limit  # cheque especial

    @property
    def overdraft_limit(self):
        return self._overdraft_limit

    def withdraw(self, amount):
        # count previous withdrawals on this account
        withdrawals_done = sum(1 for t in self.history.transactions if t["type"] == Withdrawal.__name__)

        exceeded_tx_limit = amount > self._per_tx_limit
        exceeded_withdrawals = withdrawals_done >= self._withdraw_limit
        exceeded_available = amount > (self.balance + self._overdraft_limit)

        if exceeded_available:
            print("\n@@@ Operation failed! Not enough balance or overdraft available. @@@")
            return False

        if exceeded_tx_limit:
            print("\n@@@ Operation failed! Withdrawal amount exceeds per-transaction limit. @@@")
            return False

        if exceeded_withdrawals:
            print("\n@@@ Operation failed! Maximum number of withdrawals exceeded. @@@")
            return False

        if amount <= 0:
            print("\n@@@ Operation failed! Invalid amount. @@@")
            return False

        # allow overdraft usage
        self._balance -= amount
        print("\n=== Withdrawal successful! ===")
        if self._balance < 0:
            print(f"*** Warning: You are using overdraft! Current balance: R$ {self._balance:.2f}")
        return True

    def __str__(self):
        retu

