from pydantic import BaseModel, field_validator

# 1. The Data Model (The "What")
class Payment(BaseModel):
    amount: float
    currency: str
    gateway: str

    @field_validator("amount")
    @classmethod
    def must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Payment must be greater than zero")
        return v

# 2. The Service Class (The "How")
class PaymentProcessor:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def execute_transaction(self, payment: Payment):
        # Because we used BaseModel, we KNOW 'payment' is valid here.
        # We don't need to check if amount > 0; the model already did it.
        print(f"Processing ${payment.amount} via {payment.gateway}...")
        # ... logic to call Stripe or PayPal API ...
        return {"status": "success"}

# Execution
data = {"amount": 50.0, "currency": "USD", "gateway": "Stripe"}
payment_data = Payment(**data) # Validation happens here

processor = PaymentProcessor(api_key="sk_test_123")
processor.execute_transaction(payment_data)