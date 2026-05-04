from pydantic import BaseModel, field_validator, model_validator


class Cashier(BaseModel):
    name: str
    employee_id: int
    shift: str

    @field_validator("shift")
    @classmethod
    def validate_shift(cls, v: str) -> str:
        valid = {"Morning", "Afternoon", "Evening", "Night"}
        if v not in valid:
            raise ValueError(f"shift must be one of {valid}, got '{v}'")
        return v

    def greet_customer(self, customer_name: str) -> str:
        return f"Hello {customer_name}, welcome to our store! I'm {self.name} and I'll be assisting you today."


class Product(BaseModel):
    id: str
    name: str
    price: float
    stock: int

    @field_validator("price")
    @classmethod
    def validate_price(cls, v: float) -> float:
        if v < 0:
            raise ValueError("price cannot be negative")
        return v

    @field_validator("stock")
    @classmethod
    def validate_stock(cls, v: int) -> int:
        if v < 0:
            raise ValueError("stock cannot be negative")
        return v

    def is_in_stock(self) -> bool:
        return self.stock > 0
    
class Item(BaseModel):
    name: str
    amount: int
    bought_price: float = 0.0

class Buyer(BaseModel):
    name: str
    money: float
    bought_items: list[Item] = []

    @model_validator(mode="after")
    def validate_money(self) -> "Buyer":
        if self.money < 0:
            raise ValueError("money cannot be negative")
        return self

    def list_bought_items(self) -> str:
        if not self.bought_items:
            return f"{self.name} haven't bought anything yet."
        return f"{self.name} bought items: " + ", ".join(f"{item.amount} x {item.name}" for item in self.bought_items)

    def __repr__(self) -> str:
        return f"Buyer(name={self.name!r}, money={self.money}, items={self.bought_items})"

class Cart(BaseModel):
    buyer: Buyer
    items: list[Item] = []

class Store(BaseModel):
    name: str
    balance: float = 0.0
    products: dict[str, Product] = {}
    cashiers: dict[int, Cashier] = {}

    def add_balance(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("amount must be positive")
        self.balance += amount

    def remove_balance(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("amount must be positive")
        if amount > self.balance:
            raise ValueError("Not enough balance in the store")
        self.balance -= amount

    def add_product(self, product: Product) -> None:
        self.products[product.id] = product

    def remove_product(self, product_id: str) -> None:
        if product_id in self.products:
            del self.products[product_id]

    def add_cashier(self, cashier: Cashier) -> None:
        self.cashiers[cashier.employee_id] = cashier

    def remove_cashier(self, employee_id: int) -> None:
        if employee_id in self.cashiers:
            del self.cashiers[employee_id]

    def purchase_product(
        self, cart: Cart, cashier: Cashier | None = None
    ) -> None:
        buyer = cart.buyer
        if cashier:
            print(cashier.greet_customer(buyer.name))
            
        # First pass to validate all items and calculate total cost
        total_cost = 0.0
        for item in cart.items:
            product_id = item.name
            quantity = item.amount
            if product_id not in self.products:
                raise ValueError(f"Product {product_id} not found")
                
            product = self.products[product_id]
            if not product.is_in_stock():
                raise ValueError(f"Product {product.name} is out of stock")
            if quantity > product.stock:
                raise ValueError(f"Requested quantity ({quantity}) for {product.name} exceeds available stock ({product.stock})")
                
            total_cost += product.price * quantity
            
        if buyer.money < total_cost:
            raise ValueError("Insufficient funds")
            
        # Second pass to complete the transaction
        buyer.money -= total_cost
        self.add_balance(total_cost)
        
        for item in cart.items:
            product_id = item.name
            quantity = item.amount
            product = self.products[product_id]
            product.stock -= quantity
            buyer.bought_items.append(Item(name=product.name, amount=quantity, bought_price=product.price))
            print(f"{buyer.name} bought {quantity} x {product.name} for ${product.price * quantity:.2f}")

    def restock_product(self, product_id: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("restock quantity must be positive")
        if product_id not in self.products:
            raise ValueError("Product not found")
        self.products[product_id].stock += quantity

    def __repr__(self) -> str:
        return f"Store(name={self.name!r}, balance={self.balance}, products={len(self.products)}, cashiers={len(self.cashiers)})"


def _create_store(
    name: str,
    initial_balance: float = 0.0,
    initial_products: list[Product] | None = None,
    initial_cashiers: list[Cashier] | None = None,
) -> Store:
    initial_products = initial_products or []
    initial_cashiers = initial_cashiers or []
    return Store(
        name=name,
        balance=initial_balance,
        products={p.id: p for p in initial_products},
        cashiers={c.employee_id: c for c in initial_cashiers},
    )



cashier_kevin = Cashier(name="Kevin", employee_id=101, shift="Morning")
cashier_alice = Cashier(name="Alice", employee_id=102, shift="Evening")

foods = Product(id="p1", name="Bread", price=2.5, stock=100)
drinks = Product(id="p2", name="Milk", price=1.5, stock=50)
store = _create_store(
    name="SuperMart",
    initial_balance=1000.0,
    initial_products=[foods, drinks],
    initial_cashiers=[cashier_kevin, cashier_alice],
)

buyer_john = Buyer(name="John", money=20.0)
print(buyer_john.list_bought_items())

johns_cart = Cart(
    buyer=buyer_john,
    items=[
        Item(name="p1", amount=2),
        Item(name="p2", amount=1)
    ]
)
store.purchase_product(johns_cart, cashier=cashier_kevin)
print(buyer_john.list_bought_items())
