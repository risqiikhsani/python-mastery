from models.product import Product
from models.user import User
from repositories.sql import SQLOrderRepository
from repositories.memory import InMemoryOrderRepository
from services.order_service import OrderService
from services.user_service import UserService

sql = SQLOrderRepository()
memory = InMemoryOrderRepository()  # For testing purposes, you can switch to this repository
product1 = Product(name="Laptop", price=999.99, description="A high-performance laptop.")
product2 = Product(name="Smartphone", price=499.99, description="A latest model smartphone.")
products = [product1, product2]
order_service = OrderService(order_repository=sql)
user_service = UserService(order_repository=sql)
purchaser = User(name="Alice", email="alice@example.com")

# create order
new_order = order_service.create_order(products=products, purchaser=purchaser)
print(f"Created order with ID: {new_order.id} and total price: ${new_order.total_price():.2f} and purchaser: {new_order.purchaser}")

# pay for order
payment_success = order_service.pay_for_order(order_id=new_order.id, payment_method="credit_card")
if payment_success:
    print(f"Order {new_order.id} has been paid successfully.")
else:
    print(f"Payment for order {new_order.id} failed.")

# show what the purchaser bought
items = user_service.get_items_bought(purchaser.id)
print(f"Items bought by {purchaser.name}: {[p.name for p in items]}")
