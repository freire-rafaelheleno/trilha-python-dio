import textwrap


def menu():
    menu = """\n
    ================ MENU ================
    [1]\tDeposit
    [2]\tWithdraw
    [3]\tStatement
    [4]\tNew Account
    [5]\tList Accounts
    [6]\tNew User
    [7]\tList Users
    [8]\tCheck Overdraft Balance
    [9]\tExit
    => """
    return input(textwrap.dedent(menu))


def deposit(balance, amount, statement, /):
    if amount > 0:
        balance += amount
        statement += f"Deposit:\tR$ {amount:.2f}\n"
        print("\n=== Deposit successful! ===")
    else:
        print("\n@@@ Operation failed! Invalid amount. @@@")

    return balance, statement


def withdraw(*, balance, amount, statement, limit, withdraw_count, max_withdraws, overdraft):
    exceeded_available = amount > (balance + overdraft)
    exceeded_limit = amount > limit
    exceeded_withdraws = withdraw_count >= max_withdraws

    if exceeded_available:
        print("\n@@@ Operation failed! Not enough balance or overdraft available. @@@")

    elif exceeded_limit:
        print("\n@@@ Operation failed! Withdrawal amount exceeds transaction limit. @@@")

    elif exceeded_withdraws:
        print("\n@@@ Operation failed! Maximum number of withdrawals exceeded. @@@")

    elif amount > 0:
        balance -= amount
        statement += f"Withdrawal:\tR$ {amount:.2f}\n"
        withdraw_count += 1
        print("\n=== Withdrawal successful! ===")
        if balance < 0:
            print(f"*** Warning: You are using overdraft! Current balance: R$ {balance:.2f}")

    else:
        print("\n@@@ Operation failed! Invalid amount. @@@")

    return balance, statement, withdraw_count


def show_statement(balance, /, *, statement, overdraft):
    print("\n================ STATEMENT ================")
    print("No transactions were made." if not statement else statement)
    print(f"\nBalance:\tR$ {balance:.2f}")
    if balance < 0:
        print(f"Overdraft used:\tR$ {-balance:.2f} (limit: R$ {overdraft:.2f})")
    print("===========================================")


def create_user(users):
    cpf = input("Enter CPF (numbers only): ")
    user = filter_user(cpf, users)

    if user:
        print("\n@@@ A user with this CPF already exists! @@@")
        return

    name = input("Enter full name: ")
    birth_date = input("Enter birth date (dd-mm-yyyy): ")
    address = input("Enter address (street, number - district - city/state): ")

    users.append({"name": name, "birth_date": birth_date, "cpf": cpf, "address": address})

    print("=== User created successfully! ===")


def filter_user(cpf, users):
    filtered_users = [user for user in users if user["cpf"] == cpf]
    return filtered_users[0] if filtered_users else None


def create_account(branch, account_number, users):
    cpf = input("Enter user CPF: ")
    user = filter_user(cpf, users)

    if user:
        print("\n=== Account created successfully! ===")
        return {"branch": branch, "account_number": account_number, "user": user}

    print("\n@@@ User not found, account creation canceled! @@@")


def list_accounts(accounts):
    for account in accounts:
        line = f"""\
            Branch:\t\t{account['branch']}
            Account:\t{account['account_number']}
            Holder:\t\t{account['user']['name']}
        """
        print("=" * 100)
        print(textwrap.dedent(line))


def list_users(users):
    if not users:
        print("\n@@@ No users registered. @@@")
        return
    for user in users:
        line = f"""\
            Name:\t\t{user['name']}
            CPF:\t\t{user['cpf']}
            Birth Date:\t{user['birth_date']}
            Address:\t{user['address']}
        """
        print("=" * 100)
        print(textwrap.dedent(line))


def check_overdraft(balance, overdraft):
    overdraft_used = -balance if balance < 0 else 0
    overdraft_remaining = overdraft - overdraft_used
    print("\n============ OVERDRAFT BALANCE ============")
    print(f"Overdraft limit:\tR$ {overdraft:.2f}")
    print(f"Overdraft used:\t\tR$ {overdraft_used:.2f}")
    print(f"Overdraft remaining:\tR$ {overdraft_remaining:.2f}")
    print("===========================================")


def main():
    MAX_WITHDRAWS = 3
    BRANCH = "0001"

    balance = 0
    limit = 500
    overdraft = 1000
    statement = ""
    withdraw_count = 0
    users = []
    accounts = []

    while True:
        option = menu()

        if option == "1":
            amount = float(input("Enter deposit amount: "))
            balance, statement = deposit(balance, amount, statement)

        elif option == "2":
            amount = float(input("Enter withdrawal amount: "))
            balance, statement, withdraw_count = withdraw(
                balance=balance,
                amount=amount,
                statement=statement,
                limit=limit,
                withdraw_count=withdraw_count,
                max_withdraws=MAX_WITHDRAWS,
                overdraft=overdraft,
            )

        elif option == "3":
            show_statement(balance, statement=statement, overdraft=overdraft)

        elif option == "4":
            account_number = len(accounts) + 1
            account = create_account(BRANCH, account_number, users)
            if account:
                accounts.append(account)

        elif option == "5":
            list_accounts(accounts)

        elif option == "6":
            create_user(users)

        elif option == "7":
            list_users(users)

        elif option == "8":
            check_overdraft(balance, overdraft)

        elif option == "9":
            print("Exiting... Thank you for using our banking system!")
            break

        else:
            print("Invalid option, please select a valid operation.")


main()
