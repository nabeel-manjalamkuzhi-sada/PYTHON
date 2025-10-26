def view():
    print("Function: View all accounts.\n")
    for acc_no, details in accounts.items():
        print(f"Account Number: {acc_no}")
        print(f"Name: {details['name']}")
        print(f"Balance: ₹{details['balance']:.2f}\n")
    input("Press Enter to continue...\n")

def create():
    try:
        acc_no = input("Enter new account number: ")
        if acc_no in accounts:
            print("Account number already exists.")
            input()
            return
        name = input("Enter account holder's name: ")
        deposit = float(input("Enter initial deposit amount: "))
        if deposit < 0:
            print("Initial deposit cannot be negative.")
        else:
            accounts[acc_no] = {"name": name, "balance": deposit}
            print("Account created successfully.")
    except ValueError:
        print("Invalid input. Please enter a valid amount.")
    input("Press Enter to continue...\n")

def deposit():
    try:
        acc_no = input("Enter account number to deposit into: ")
        if acc_no in accounts:
            amount = float(input("Enter amount to deposit: "))
            if amount < 0:
                print("Cannot deposit a negative amount.")
            else:
                accounts[acc_no]["balance"] += amount
                print("Deposit successful.")
        else:
            print("Account not found.")
    except ValueError:
        print("Invalid input. Please enter a valid amount.")
    input("Press Enter to continue...\n")

def withdraw():
    try:
        acc_no = input("Enter account number to withdraw from: ")
        if acc_no in accounts:
            amount = float(input("Enter amount to withdraw: "))
            if amount < 0:
                print("Cannot withdraw a negative amount.")
            elif amount > accounts[acc_no]["balance"]:
                print("Insufficient balance.")
            else:
                accounts[acc_no]["balance"] -= amount
                print("Withdrawal successful.")
        else:
            print("Account not found.")
    except ValueError:
        print("Invalid input. Please enter a valid amount.")
    input("Press Enter to continue...\n")

def check():
    acc_no = input("Enter account number to check balance: ")
    if acc_no in accounts:
        print(f"Account Holder: {accounts[acc_no]['name']}")
        print(f"Balance: ₹{accounts[acc_no]['balance']:.2f}")
    else:
        print("Account not found.")
    input("Press Enter to continue...\n")

def Exit():
    print("Exiting the banking system...")

# Main menu
flag = 0
accounts = {
    "1001": {"name": "Alice", "balance": 5000.0},
    "1002": {"name": "Bob", "balance": 3200.0}
}

while flag == 0:
    try:
        print("\n==== Simple Banking System ====")
        print("1. View All Accounts")
        print("2. Create New Account")
        print("3. Deposit Money")
        print("4. Withdraw Money")
        print("5. Check Balance")
        print("6. Exit\n")

        e = int(input("Enter option number: "))
        print("\n")
        if e == 1:
            view()
        elif e == 2:
            create()
        elif e == 3:
            deposit()
        elif e == 4:
            withdraw()
        elif e == 5:
            check()
        elif e == 6:
            Exit()
            flag = 1
        else:
            print("Invalid option.")
    except ValueError:
        print("Enter correct option only.")

print("Program has ended.")
