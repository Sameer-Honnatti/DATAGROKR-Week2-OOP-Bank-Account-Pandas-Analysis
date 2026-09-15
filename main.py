from banking.accounts import (
    SavingsAccount,
    CurrentAccount,
    InsufficientBalanceError,
    InvalidAmountError
)

from analytics.reports import BankDataAnalyzer

from pathlib import Path

DATA_DIR = Path("data")

CUSTOMERS_FILE = DATA_DIR / "customers.csv"
TRANSACTIONS_FILE = DATA_DIR / "transactions.csv"

analyzer = BankDataAnalyzer(
    CUSTOMERS_FILE,
    TRANSACTIONS_FILE
)

accounts = {}


def create_account():
    print("\n===== CREATE ACCOUNT =====")

    account_number = input("Enter account number: ").strip()
    holder_name = input("Enter account holder name: ").strip()

    if account_number in accounts:
        print("Account already exists.")
        return

    print("\n1. Savings Account")
    print("2. Current Account")

    choice = input("Enter account type: ").strip()

    try:
        initial_balance = float(input("Enter initial balance: "))

        if choice == "1":
            account = SavingsAccount(
                account_number,
                holder_name,
                initial_balance
            )
        elif choice == "2":
            account = CurrentAccount(
                account_number,
                holder_name,
                initial_balance
            )
        else:
            print("Invalid account type.")
            return

        accounts[account_number] = account
        print("Account created successfully.")

    except ValueError:
        print("Please enter a valid amount.")
    except InvalidAmountError as error:
        print(f"Error: {error}")


def find_account():
    account_number = input("Enter account number: ").strip()

    account = accounts.get(account_number)

    if account is None:
        print("Account not found.")

    return account


def deposit_money():
    print("\n===== DEPOSIT MONEY =====")

    account = find_account()

    if account is None:
        return

    try:
        amount = float(input("Enter deposit amount: "))
        balance = account.deposit(amount)
        print(f"Deposit successful.")
        print(f"Current balance: {balance:.2f}")

    except ValueError:
        print("Please enter a valid amount.")
    except InvalidAmountError as error:
        print(f"Error: {error}")


def withdraw_money():
    print("\n===== WITHDRAW MONEY =====")

    account = find_account()

    if account is None:
        return

    try:
        amount = float(input("Enter withdrawal amount: "))
        balance = account.withdraw(amount)
        print("Withdrawal successful.")
        print(f"Current balance: {balance:.2f}")

    except ValueError:
        print("Please enter a valid amount.")
    except InsufficientBalanceError as error:
        print(f"Error: {error}")
    except InvalidAmountError as error:
        print(f"Error: {error}")


def view_account():
    print("\n===== ACCOUNT DETAILS =====")

    account = find_account()

    if account is None:
        return

    details = account.get_details()

    for key, value in details.items():
        if key == "balance":
            print(f"{key.replace('_', ' ').title()}: {value:.2f}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")


def show_all_accounts():
    print("\n===== ALL ACCOUNTS =====")

    if not accounts:
        print("No accounts available.")
        return

    account_details = [
        account.get_details()
        for account in accounts.values()
    ]

    for details in account_details:
        print(
            f"{details['account_number']} | "
            f"{details['holder_name']} | "
            f"{details['account_type']} | "
            f"{details['balance']:.2f}"
        )


def show_transaction_summary():
    print("\n===== TRANSACTION SUMMARY =====")

    summary = analyzer.transaction_summary()

    print(summary.to_string(index=False))


def show_customer_summary():
    print("\n===== CUSTOMER SUMMARY =====")

    summary = analyzer.customer_summary()

    print(summary.to_string(index=False))


def show_branch_summary():
    print("\n===== BRANCH SUMMARY =====")

    summary = analyzer.branch_summary()

    print(summary.to_string(index=False))


def show_numpy_statistics():
    print("\n===== NUMPY STATISTICS =====")

    statistics = analyzer.numpy_statistics()

    for key, value in statistics.items():
        print(f"{key.replace('_', ' ').title()}: {value:.2f}")


def show_high_value_transactions():
    print("\n===== HIGH VALUE TRANSACTIONS =====")

    try:
        threshold = float(
            input("Enter minimum transaction amount: ")
        )

        result = analyzer.high_value_transactions(threshold)

        if result.empty:
            print("No transactions found.")
        else:
            print(result.to_string(index=False))

    except ValueError:
        print("Please enter a valid amount.")


def show_filtered_customers():
    print("\n===== HIGH VALUE CUSTOMERS =====")

    customers = analyzer.filtered_customers()

    if not customers:
        print("No high-value customers found.")
        return

    for customer in customers:
        print(
            f"Customer ID: {customer['customer_id']} | "
            f"Name: {customer['customer_name']} | "
            f"Total: {customer['sum']:.2f}"
        )


def show_account_type_statistics():
    print("\n===== ACCOUNT TYPE STATISTICS =====")

    statistics = analyzer.account_type_statistics()

    for account_type, total in statistics.items():
        print(f"{account_type}: {total:.2f}")


def show_top_customers():
    print("\n===== TOP CUSTOMERS =====")

    result = analyzer.top_customers()

    print(result.to_string(index=False))


def show_sorted_transactions():
    print("\n===== SORTED TRANSACTIONS =====")

    transactions = analyzer.sorted_transactions()

    for transaction in transactions[:10]:
        print(
            f"{transaction['transaction_id']} | "
            f"{transaction['customer_id']} | "
            f"{transaction['transaction_type']} | "
            f"{transaction['amount']:.2f}"
        )


def show_menu():
    print("\n" + "=" * 50)
    print("           DATA GROKR BANK SYSTEM")
    print("=" * 50)
    print("1. Create Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. View Account")
    print("5. View All Accounts")
    print("6. Transaction Summary")
    print("7. Customer Summary")
    print("8. Branch Summary")
    print("9. NumPy Statistics")
    print("10. High Value Transactions")
    print("11. High Value Customers")
    print("12. Account Type Statistics")
    print("13. Top Customers")
    print("14. Sorted Transactions")
    print("15. Exit")
    print("=" * 50)


def main():
    print("=" * 50)
    print("       DATA GROKR BANK ACCOUNT SYSTEM")
    print("=" * 50)

    while True:
        show_menu()

        choice = input("Enter your choice: ").strip()

        actions = {
            "1": create_account,
            "2": deposit_money,
            "3": withdraw_money,
            "4": view_account,
            "5": show_all_accounts,
            "6": show_transaction_summary,
            "7": show_customer_summary,
            "8": show_branch_summary,
            "9": show_numpy_statistics,
            "10": show_high_value_transactions,
            "11": show_filtered_customers,
            "12": show_account_type_statistics,
            "13": show_top_customers,
            "14": show_sorted_transactions
        }

        if choice == "15":
            print("\nThank you for using Data Grokr Bank System!")
            break

        action = actions.get(choice)

        if action:
            try:
                action()
            except Exception as error:
                print(f"Unexpected error: {error}")
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()