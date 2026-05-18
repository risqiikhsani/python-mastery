from abc import ABC, abstractmethod
from pydantic import BaseModel

# 1. Open/Closed Principle (OCP) - Strategy Pattern for Discounts

class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, amount: float) -> float:
        pass

class NoDiscount(DiscountStrategy):
    def apply_discount(self, amount: float) -> float:
        return amount
    
class BasicDiscount(DiscountStrategy):
    def apply_discount(self, amount: float) -> float:
        return amount * 0.80

class VIPDiscount(DiscountStrategy):
    def apply_discount(self, amount: float) -> float:
        return amount * 0.50
    
# 2. Dependency Inversion / Single Responsibility

class OrderItem(BaseModel):
    name: str
    price: float
    quantity: int

class OrderData(BaseModel):
    items: list[OrderItem]
    total: float
    final_total: float

class OrderRepository:
    @abstractmethod
    def save(self, order_data: OrderData):
        pass

class SQLOrderRepository(OrderRepository):
    def save(self, order_data: OrderData):
        print(f"Saving order to SQL database: {order_data.model_dump()}")

class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self.orders: list[OrderData] = []
    
    def save(self, order_data: OrderData):
        self.orders.append(order_data)
        print(f"Order saved in memory: {order_data.model_dump()}")

# 3. The Refactored Order Processor

class OrderProcessor:
    def __init__(self, discount_strategy: DiscountStrategy, repository: OrderRepository):
        self.discount_strategy = discount_strategy
        self.repository = repository

    def process(self, items: list[OrderItem]) -> float:
        validated_items = [OrderItem.model_validate(item) for item in items]
        total = sum(item.price * item.quantity for item in validated_items)

        final_total = self.discount_strategy.apply_discount(total)

        order_data = OrderData(
            items=validated_items,
            total=total,
            final_total=final_total,
        )

        self.repository.save(order_data)
        return final_total


cart_items = [
    {"name": "Laptop", "price": 1000.0, "quantity": 1},
    {"name": "Mouse", "price": 50.0, "quantity": 2},
]

user1 = OrderProcessor(discount_strategy=VIPDiscount(), repository=SQLOrderRepository())
total = user1.process(cart_items)
print(f"Final total for VIP user: ${total:.2f}")

user2 = OrderProcessor(discount_strategy=BasicDiscount(), repository=InMemoryOrderRepository())
total = user2.process(cart_items)
print(f"Final total for Basic user: ${total:.2f}")