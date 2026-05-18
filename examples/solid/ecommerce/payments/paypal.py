from .payment import PaymentProcessor

class PayPalPaymentProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        # Simulate PayPal payment processing logic
        print(f"Processing PayPal payment of ${amount:.2f}...")
        # Here you would integrate with the PayPal API to process the payment
        # For this example, we'll assume the payment is always successful
        print("PayPal payment processed successfully.")
        return True