from .product import Product
from .user import User
import uuid

class Order:
    def __init__(self, products: list[Product], purchaser: User | None = None):
        self.id = uuid.uuid4().hex
        self.products = products
        self.is_paid = False
        self.purchaser = purchaser

    def total_price(self) -> float:
        return sum(product.price for product in self.products)

    def mark_paid(self):
        self.is_paid = True

    def set_purchaser(self, purchaser: User):
        self.purchaser = purchaser