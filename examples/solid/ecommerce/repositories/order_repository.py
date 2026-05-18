from abc import ABC, abstractmethod
from models.order import Order

class OrderRepository(ABC):

    @abstractmethod
    def create_order(self, order: Order) -> Order:
        """Persists a new order and returns the created order with an assigned ID (string)."""
        pass

    @abstractmethod
    def get_order_by_id(self, order_id: str) -> Order:
        """Retrieves an order by its unique identifier (string)."""
        pass

    @abstractmethod
    def update_order(self, order: Order) -> Order:
        """Updates an existing order's details and returns the updated order."""
        pass

    @abstractmethod
    def delete_order(self, order_id: str) -> None:
        """Removes an order from the repository based on its ID (string)."""
        pass

    @abstractmethod
    def get_orders_by_user(self, user_id: str) -> list[Order]:
        """Retrieve all orders associated with a given user id (string)."""
        pass