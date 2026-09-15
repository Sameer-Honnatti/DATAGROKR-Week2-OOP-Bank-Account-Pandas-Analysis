from functools import wraps
from .context import TransactionLogger

def transaction(function):
    @wraps(function)
    def wrapper(self, amount):
        result = function(self, amount)
        with TransactionLogger("logs/transactions.txt") as logger:
            logger.write(
                f"{function.__name__.upper()} | "
                f"Account: {self.account_number} | "
                f"Holder: {self.holder_name} | "
                f"Amount: {amount:.2f} | "
                f"Balance: {self.balance:.2f}"
            )
        return result
    return wrapper