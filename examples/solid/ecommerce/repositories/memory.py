from .order_repository import OrderRepository
import uuid

class InMemoryOrderRepository(OrderRepository):

    def __init__(self):
        self.orders = {}

    def create_order(self, order):
        self.orders[order.id] = order
        return order

    def get_order_by_id(self, order_id):
        return self.orders.get(order_id)

    def update_order(self, order):
        if order.id in self.orders:
            self.orders[order.id] = order
            return order
        raise ValueError("Order not found")

    def delete_order(self, order_id):
        if order_id in self.orders:
            del self.orders[order_id]
        else:
            raise ValueError("Order not found")

    def get_orders_by_user(self, user_id: str):
        result = []
        for order in self.orders.values():
            purchaser = getattr(order, "purchaser", None)
            if purchaser and getattr(purchaser, "id", None) == user_id:
                result.append(order)
        return result