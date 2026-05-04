"""
Design Patterns: Strategy
"""

from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass


class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str):
        self.card_number = card_number

    def pay(self, amount: float) -> bool:
        print(f"Paid ${amount:.2f} with credit card ending in {self.card_number[-4:]}")
        return True


class PayPalPayment(PaymentStrategy):
    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float) -> bool:
        print(f"Paid ${amount:.2f} via PayPal ({self.email})")
        return True


class CryptoPayment(PaymentStrategy):
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address

    def pay(self, amount: float) -> bool:
        print(f"Paid ${amount:.2f} in crypto to wallet {self.wallet_address[:10]}...")
        return True


class ShoppingCart:
    def __init__(self):
        self.items: list[tuple[str, float]] = []
        self.payment_strategy: PaymentStrategy | None = None

    def add_item(self, name: str, price: float):
        self.items.append((name, price))

    def total(self) -> float:
        return sum(price for _, price in self.items)

    def set_payment(self, strategy: PaymentStrategy):
        self.payment_strategy = strategy

    def checkout(self) -> bool:
        if not self.payment_strategy:
            raise ValueError("No payment method set")
        if not self.items:
            print("Cart is empty")
            return False
        return self.payment_strategy.pay(self.total())


# Usage
cart = ShoppingCart()
cart.add_item("Laptop", 999.99)
cart.add_item("Mouse", 29.99)

cart.set_payment(CreditCardPayment("4111111111111111"))
cart.checkout()

print()
cart.set_payment(PayPalPayment("user@email.com"))
cart.checkout()