from .payment import PaymentProcessor

class CreditCardPaymentProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        # Simulate credit card payment processing logic
        print(f"Processing credit card payment of ${amount:.2f}...")
        # Here you would integrate with a credit card payment gateway API to process the payment
        # For this example, we'll assume the payment is always successful
        print("Credit card payment processed successfully.")
        return True