from .decorators import transaction

class BankError(Exception):
    pass

class InsufficientBalanceError(BankError):
    pass

class InvalidAmountError(BankError):
    pass

class BankAccount:
    bank_name = "Data Grokr Bank"

    def __init__(self, account_number, holder_name, balance=0):
        self.account_number = account_number
        self.holder_name = holder_name
        self.balance = float(balance)

    @transaction
    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be greater than zero.")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        raise NotImplementedError("Withdraw method must be implemented by subclasses.")

    def get_details(self):
        return {
            "account_number": self.account_number,
            "holder_name": self.holder_name,
            "account_type": self.__class__.__name__,
            "balance": self.balance
        }

class SavingsAccount(BankAccount):
    def __init__(self, account_number, holder_name, balance=0, minimum_balance=500):
        super().__init__(account_number, holder_name, balance)
        self.minimum_balance = float(minimum_balance)

    @transaction
    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be greater than zero.")
        if self.balance - amount < self.minimum_balance:
            raise InsufficientBalanceError(
                f"Minimum balance of {self.minimum_balance:.2f} must be maintained."
            )
        self.balance -= amount
        return self.balance

class CurrentAccount(BankAccount):
    def __init__(self, account_number, holder_name, balance=0, overdraft_limit=5000):
        super().__init__(account_number, holder_name, balance)
        self.overdraft_limit = float(overdraft_limit)

    @transaction
    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be greater than zero.")
        if amount > self.balance + self.overdraft_limit:
            raise InsufficientBalanceError(
                f"Overdraft limit of {self.overdraft_limit:.2f} exceeded."
            )
        self.balance -= amount
        return self.balance