from repositories.order_repository import OrderRepository
from models.product import Product


class UserService:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def get_items_bought(self, user_id: str, only_paid: bool = True) -> list[Product]:
        """Return a list of Product instances the user bought across their orders.

        Args:
            user_id: the user's id string
            only_paid: if True, include only paid orders
        """
        orders = self.order_repository.get_orders_by_user(user_id)
        items: list[Product] = []
        for order in orders:
            if only_paid and not getattr(order, "is_paid", False):
                continue
            items.extend(order.products)
        return items
