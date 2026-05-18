from models.order import Order
from models.product import Product
from repositories.order_repository import OrderRepository
from payments.payment_factory import PaymentFactory


class OrderService:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository
        self.payment_factory = PaymentFactory()

    def create_order(self, products: list[Product], purchaser=None) -> Order:
        new_order = Order(products=products, purchaser=purchaser)  # ID will be assigned by the repository
        return self.order_repository.create_order(new_order)

    def pay_for_order(self, order_id: str, payment_method: str) -> bool:
        order = self.order_repository.get_order_by_id(order_id)
        if not order:
            raise ValueError("Order not found")

        if order.is_paid:
            raise ValueError("Order is already paid")

        total_amount = order.total_price()
        payment_processor = self.payment_factory.create_payment_processor(payment_method)
        
        if payment_processor.process_payment(total_amount):
            order.mark_paid()
            self.order_repository.update_order(order)
            return True
        
        return False