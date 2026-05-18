from .paypal import PayPalPaymentProcessor
from .creditcard import CreditCardPaymentProcessor

class PaymentFactory:
    @staticmethod
    def create_payment_processor(method: str):
        if method == "credit_card":
            return CreditCardPaymentProcessor()
        elif method == "paypal":
            return PayPalPaymentProcessor()
        else:
            raise ValueError(f"Unsupported payment method: {method}")