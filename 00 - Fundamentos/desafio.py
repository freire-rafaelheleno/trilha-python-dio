menu = """

[1] Deposit
[2] Withdraw
[3] Statement
[4] Exit
[5] Check overdraft balance

=> """

balance = 0
limit = 500
overdraft = 300  # overdraft limit
statement = ""
withdraw_count = 0
MAX_WITHDRAWS = 3

while True:

    option = input(menu)

    if option == "1":
        amount = float(input("Enter the deposit amount: "))

        if amount > 0:
            balance += amount
            statement += f"Deposit: $ {amount:.2f}\n"
        else:
            print("Operation failed! Invalid amount.")

    elif option == "2":
        amount = float(input("Enter the withdrawal amount: "))

        exceeded_limit = amount > limit
        exceeded_withdraws = withdraw_count >= MAX_WITHDRAWS
        exceeded_available = amount > (balance + overdraft)

        if exceeded_available:
            print("Operation failed! Not enough balance or overdraft available.")

        elif exceeded_limit:
            print("Operation failed! Withdrawal amount exceeds transaction limit.")

        elif exceeded_withdraws:
            print("Operation failed! Maximum number of withdrawals exceeded.")

        elif amount > 0:
            balance -= amount
            if balance < 0:
                print(f"Warning: You are using your overdraft! Current balance: $ {balance:.2f}")
            statement += f"Withdrawal: $ {amount:.2f}\n"
            withdraw_count += 1
        else:
            print("Operation failed! Invalid amount.")

    elif option == "3":
        print("\n================ STATEMENT ================")
        print("No transactions were made." if not statement else statement)
        print(f"\nBalance: $ {balance:.2f}")
        if balance < 0:
            print(f"Overdraft used: $ {-balance:.2f} (limit: $ {overdraft:.2f})")
        print("===========================================")

    elif option == "4":
        print("Exiting... Thank you for using our bank system!")
        break

    elif option == "5":
        overdraft_used = -balance if balance < 0 else 0
        overdraft_remaining = overdraft - overdraft_used
        print("\n============ OVERDRAFT BALANCE ============")
        print(f"Overdraft limit: $ {overdraft:.2f}")
        print(f"Overdraft used: $ {overdraft_used:.2f}")
        print(f"Overdraft remaining: $ {overdraft_remaining:.2f}")
        print("===========================================")

    else:
        print("Invalid option, please select a valid operation.")

