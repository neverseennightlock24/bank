import json
import os
from datetime import datetime

class BankAccount:
    def __init__(self, balance, name, transactions = None):
        self.balance = balance
        self.name = name
        self.transactions = transactions if transactions is not None else []

    def add_balance(self):
        try:
            deposit = float(input("What would you like to add to your balance? $"))
            if deposit < 0:
                print("You cannot deposit a negative amount. ")
            else:
                self.balance += deposit
                self.transactions.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Deposit", deposit))
                print(f"Your new balance is ${self.balance:.2f}")
        except ValueError:
            print("Invalid input. Please enter a numeric value. ")

    def subtract_balance(self):
        try:
            withdraw = float(input("What would you like to remove from your balance? $"))
            if withdraw < 0:
                print("You cannot withdraw a negative amount.")
            elif withdraw > self.balance:
                print("Insufficient funds.")
            else:
                self.balance -= withdraw
                self.transactions.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Withdrawal", -withdraw))
                print(f"Your new balance is ${self.balance:.2f}")
        except ValueError:
            print("Invalid input. Please enter a numeric value. ")

    def check_balance(self):
        print(f"{self.name}'s bank account balance is ${self.balance:.2f}")

    def view_transactions(self):
        if not self.transactions:
            print("No transactions available. ")
        else:
            print("Transaction History:")
            for date, type, amount in self.transactions:
                print(f"{date}: {type} of ${amount:.2f}")

    def calculate_interest(self, rate):
        interest = self.balance * rate / 100
        self.balance += interest
        self.transactions.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Interest", interest))
        print(f"Interest added at {rate}% rate. Your new balance is ${self.balance:.2f}")

    def transfer_funds(self, target_account, amount):
        if target_account == self:
            print("You cannot transfer money to yourself.")
            return
        if amount > self.balance:
            print("Insufficient funds for transfer.")
        elif amount < 0:
            print("You cannot transfer a negative amount.")
        else:
            self.balance -= amount
            target_account.balance += amount
            self.transactions.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Transfer Out", -amount))
            target_account.transactions.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Transfer In", amount))
            print(f"Transferred ${amount:.2f} to {target_account.name}. Your new balance is ${self.balance:.2f}")

    def change_name(self, new_name):
        self.name = new_name
        print(f"Your account name has been changed to {new_name}.")

    def to_dict(self):
        return {"balance": self.balance, "name": self.name, "transactions": self.transactions}

    @staticmethod
    def from_dict(data):
        return BankAccount(data["balance"], data["name"], data.get("transactions", []))

def load_accounts(filename="accounts.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def save_accounts(accounts, filename="accounts.json"):
    with open(filename, "w") as file:
        json.dump(accounts, file, indent = 4)

def main():
    accounts = load_accounts()

    while True:
        user_name = input("Hello, new customer. What is your name? ")

        if user_name in accounts:
            bank_user = BankAccount.from_dict(accounts[user_name])
            print(f"Welcome back, {user_name}. ")
            break
        else:
            create_new = input(f"The name '{user_name}' is not in our records. Would you like to create a new account with this name? (yes/no) ").strip().lower()
            if create_new == 'yes':
                bank_user = BankAccount(0, user_name)
                accounts[user_name] = bank_user.to_dict()
                save_accounts(accounts)
                print(f"Welcome, {user_name}. Your account has been created. ")
                break
            elif create_new == 'no':
                print("Please enter a different name.")
            else:
                print("Please choose a valid option! ")

    while True:
        user_input = input("\nPlease choose from the following options:\n"
                           "1. Check your bank account balance\n"
                           "2. Add to your bank account balance\n"
                           "3. Remove from your bank account balance\n"
                           "4. View transaction history\n"
                           "5. Calculate interest\n"
                           "6. Transfer funds\n"
                           "7. Change account name\n"
                           "8. Close bank account\n"
                           "9. End session\n"
                           "Your choice: ")

        if user_input == "1":
            bank_user.check_balance()

        elif user_input == "2":
            bank_user.add_balance()
            accounts[user_name] = bank_user.to_dict()
            save_accounts(accounts)

        elif user_input == "3":
            bank_user.subtract_balance()
            accounts[user_name] = bank_user.to_dict()
            save_accounts(accounts)

        elif user_input == "4":
            bank_user.view_transactions()

        elif user_input == "5":
            try:
                rate = float(input("Enter the interest rate (as a percentage): "))
                bank_user.calculate_interest(rate)
                accounts[user_name] = bank_user.to_dict()
                save_accounts(accounts)
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        elif user_input == "6":
            target_name = input("Enter the name of the account to transfer funds to: ")
            if target_name == user_name:
                print("You cannot transfer money to yourself.")
            elif target_name in accounts:
                target_account = BankAccount.from_dict(accounts[target_name])
                try:
                    amount = float(input("Enter the amount to transfer: $"))
                    bank_user.transfer_funds(target_account, amount)
                    accounts[user_name] = bank_user.to_dict()
                    accounts[target_name] = target_account.to_dict()
                    save_accounts(accounts)
                except ValueError:
                    print("Invalid input. Please enter a numeric value.")
            else:
                print(f"No account found with the name '{target_name}'. ")

        elif user_input == "7":
            new_name = input("Enter the new account name: ")
            if new_name in accounts:
                print(f"An account with the name '{new_name}' already exists. Please choose a different name. ")
            else:
                bank_user.change_name(new_name)
                del accounts[user_name]
                user_name = new_name
                accounts[user_name] = bank_user.to_dict()
                save_accounts(accounts)

        elif user_input == "8":
            confirm = input(f"Are you sure you want to close your account, {bank_user.name}? This action cannot be undone. (yes/no) ").strip().lower()
            if confirm == 'yes':
                del accounts[user_name]
                save_accounts(accounts)
                print(f"Your account has been closed. Thank you for banking with us, {bank_user.name}.")
                break
            else:
                print("Account closure cancelled. ")

        elif user_input == "9":
            print(f"Ending session. Thank you for banking with us, {bank_user.name}.")
            save_accounts(accounts)
            break

        else:
            print("Invalid choice. Please select a valid option. ")

    print(f"Your final account balance is ${bank_user.balance:.2f}")

if __name__ == "__main__":
    main()