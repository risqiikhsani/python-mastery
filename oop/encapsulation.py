"""
OOP: Encapsulation - private attributes, properties, data hiding
"""

class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        # Private attribute (convention: single underscore prefix)
        self._balance = balance
        # Double underscore = name mangling (harder to access)
        self.__transaction_history = []

    @property
    def balance(self) -> float:
        """Read-only property for balance."""
        return self._balance

    @balance.setter
    def balance(self, value: float):
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount
        self.__record_transaction("deposit", amount)

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        self.__record_transaction("withdrawal", amount)

    def __record_transaction(self, txn_type: str, amount: float) -> None:
        """Private method - can only be called from within the class."""
        self.__transaction_history.append((txn_type, amount))

    def get_history(self) -> list:
        """Public interface to private data."""
        return list(self.__transaction_history)


# Usage
account = BankAccount("Alice", 1000)
print(f"Balance: ${account.balance:.2f}")  # $1000.00

account.deposit(500)
print(f"New balance: ${account.balance:.2f}")  # $1500.00

account.withdraw(200)
print(f"After withdrawal: ${account.balance:.2f}")  # $1300.00

print(f"History: {account.get_history()}")

# This won't work:
# account.__transaction_history  # AttributeError!
# account.__record_transaction("test", 100)  # AttributeError!