"""
Design Patterns: Adapter
"""

# Existing class with incompatible interface
class OldPaymentSystem:
    def make_payment(self, amount: float, currency: str) -> dict:
        return {
            "status": "success",
            "transaction_id": "OLD123",
            "amount": amount,
            "currency": currency
        }


# New interface we want to use
class PaymentProcessor(Protocol):
    def process_payment(self, amount: float) -> bool: ...


from typing import Protocol


# Adapter wraps the old system
class PaymentAdapter(Protocol):
    def process_payment(self, amount: float) -> bool:
        """Process payment using new interface."""
        ...

    def refund(self, transaction_id: str) -> bool:
        """Refund a transaction."""
        ...


class OldToNewAdapter:
    def __init__(self):
        self._legacy = OldPaymentSystem()

    def process_payment(self, amount: float) -> bool:
        result = self._legacy.make_payment(amount, "USD")
        return result["status"] == "success"

    def refund(self, transaction_id: str) -> bool:
        # Assume legacy has a refund method
        print(f"Refunding transaction {transaction_id}")
        return True


# Usage
adapter = OldToNewAdapter()
if adapter.process_payment(99.99):
    print("Payment successful!")
    adapter.refund("OLD123")