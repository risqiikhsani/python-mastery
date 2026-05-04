from pydantic import BaseModel, field_validator
from abc import ABC, abstractmethod
from typing import ClassVar


# 1. Base Account (Abstract)
class Account(BaseModel, ABC):
    account_number: str
    balance: float = 0.0

    @field_validator("balance")
    @classmethod
    def non_negative_balance(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Balance cannot be negative")
        return v

    @abstractmethod
    def display_account_type(self) -> str:
        pass

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount

    def get_statement(self) -> dict:
        return {
            "account_number": self.account_number,
            "type": self.display_account_type(),
            "balance": self.balance,
        }


# 2. Savings Account (Inherits from Account)
class SavingsAccount(Account):
    interest_rate: float = 0.02

    def display_account_type(self) -> str:
        return "Savings"

    def apply_interest(self) -> float:
        interest = self.balance * self.interest_rate
        self.balance += interest
        return interest


# 3. Checking Account (Inherits from Account)
class CheckingAccount(Account):
    overdraft_limit: float = 500.0
    OVERDRAFT_FEE: ClassVar[float] = 25.0

    def display_account_type(self) -> str:
        return "Checking"

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance + self.overdraft_limit:
            raise ValueError("Exceeds overdraft limit")
        entering_overdraft = self.balance >= 0 and (self.balance - amount) < 0
        self.balance -= amount
        if entering_overdraft:
            print(f"  -> Overdraft fee of ${self.OVERDRAFT_FEE} applied")
            self.balance -= self.OVERDRAFT_FEE


# 4. Bank Service (Single entry point for all operations)
class Bank:
    def __init__(self, name: str):
        self.name = name
        self.accounts: dict[str, Account] = {}

    def open_account(self, account: Account) -> str:
        self.accounts[account.account_number] = account
        return account.account_number

    def get_account(self, account_number: str) -> Account:
        if account_number not in self.accounts:
            raise KeyError(f"Account {account_number} not found")
        return self.accounts[account_number]

    def deposit(self, account_number: str, amount: float) -> None:
        account = self.get_account(account_number)
        account.deposit(amount)

    def withdraw(self, account_number: str, amount: float) -> None:
        account = self.get_account(account_number)
        account.withdraw(amount)

    def transfer(self, from_acc: str, to_acc: str, amount: float) -> None:
        sender = self.get_account(from_acc)
        receiver = self.get_account(to_acc)
        sender.withdraw(amount)
        receiver.deposit(amount)

    def apply_interest(self, account_number: str) -> float:
        account = self.get_account(account_number)
        if not isinstance(account, SavingsAccount):
            raise TypeError("Interest can only be applied to SavingsAccount")
        return account.apply_interest()

    def get_statement(self, account_number: str) -> dict:
        return self.get_account(account_number).get_statement()



bank = Bank("Python Bank")

# Create accounts (still need the raw objects to instantiate)
savings_data = SavingsAccount(account_number="SAV-001", balance=1000.0, interest_rate=0.03)
checking_data = CheckingAccount(account_number="CHK-001", balance=500.0, overdraft_limit=200.0)

# Open via Bank (centralized control)
bank.open_account(savings_data)
bank.open_account(checking_data)

print(f"Welcome to {bank.name}\n")

# All operations go through the Bank
print("=== Savings Account ===")
interest = bank.apply_interest("SAV-001")
print(f"Applied interest: ${interest:.2f}")
print(f"New balance: ${bank.get_statement("SAV-001")["balance"]:.2f}\n")

print("=== Checking Account ===")
bank.withdraw("CHK-001", 100)
print(f"Withdrew $100. Balance: ${bank.get_statement("CHK-001")["balance"]:.2f}\n")

print("=== Overdraft Scenario ===")
bank.withdraw("CHK-001", 500)
print(f"Withdrew $500 (uses overdraft). Balance: ${bank.get_statement("CHK-001")["balance"]:.2f}")

print("=== Transfer ===")
bank.transfer("CHK-001", "SAV-001", 50)
print("Transferred $50 from checking to savings")

print("\n=== Final Statements ===")
print(bank.get_statement("SAV-001"))
print(bank.get_statement("CHK-001"))