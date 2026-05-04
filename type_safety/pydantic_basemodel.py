"""
Pydantic BaseModel — Data Validation for Classes and Objects
=============================================================

Pydantic's BaseModel is the core of Pydantic's data validation system.
It lets you define data models as Python classes with type annotations,
and Pydantic automatically validates data at runtime, parses it into
the right types, and provides serialization helpers — all without
writing a single manual validation check.
"""

from __future__ import annotations

from datetime import datetime
from pydantic import (
    BaseModel,
    Field,
    computed_field,
    field_validator,
    ConfigDict,
)


# =============================================================================
# SECTION 1: The Core Problem BaseModel Solves
# =============================================================================
# Before Pydantic, you might write manual validation like this:
#
#     def create_user(name, email, age):
#         if not isinstance(name, str):
#             raise TypeError("name must be a string")
#         if "@" not in email:
#             raise ValueError("invalid email")
#         if age < 0:
#             raise ValueError("age cannot be negative")
#         return {"name": name, "email": email, "age": age}
#
# BaseModel replaces ALL of that with declarative field definitions.
# =============================================================================


# =============================================================================
# SECTION 2: Your First BaseModel
# =============================================================================

class User(BaseModel):
    name: str
    email: str
    age: int
    active: bool = True          # default value
    roles: list[str] = Field(default_factory=list)  # mutable default via factory


if __name__ == "__main__":
    # Parsing — strings are coerced to the right type automatically
    user = User(name="Alice", email="alice@example.com", age=30)
    print(user.model_dump())
    # {'name': 'Alice', 'email': 'alice@example.com', 'age': 30, 'active': True, 'roles': []}

    # Validation failure — raises ValidationError with a clear message
    try:
        bad = User(name="Bob", email="not-an-email", age=-5)
    except Exception as e:
        print(f"Caught: {e}")
        # 2 validation errors:
        # email
        #   Input should be a valid email address ...
        # age
        #   Input should be greater than 0 ...

    # Construct from dict (e.g., from an API request or JSON payload)
    data = {"name": "Carol", "email": "carol@example.com", "age": 25}
    carol = User(**data)
    print(carol.model_dump_json())
    # {"name":"Carol","email":"carol@example.com","age":25,"active":true,"roles":[]}


# =============================================================================
# SECTION 3: Field — More Control Over Each Field
# =============================================================================

class Product(BaseModel):
    # Field(...) adds metadata: descriptions, bounds, aliases, examples
    name: str = Field(min_length=1, max_length=100, description="Product display name")
    price: float = Field(gt=0, description="Price must be positive")
    quantity: int = Field(ge=0, default=0, description="Units in stock")
    sku: str | None = Field(default=None, pattern=r"^[A-Z]{3}-\d{4}$", description="Stock-keeping unit code")


if __name__ == "__main__":
    prod = Product(name="Widget", price=9.99, quantity=100, sku="WGT-0001")
    print(prod.model_dump())

    # ValidationError on bad pattern
    try:
        Product(name="Widget", price=9.99, sku="bad-sku")
    except Exception as e:
        print(f"Bad SKU caught: {e}")


# =============================================================================
# SECTION 4: Validators — Transform and Check Data
# =============================================================================
# field_validator runs on a single field; model_validator runs on the whole model.

class Registration(BaseModel):
    username: str
    email: str
    password: str
    created_at: datetime | None = None

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("username must be alphanumeric")
        return v.lower()

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("password must be at least 8 characters")
        return v  # stored as-is (in production, hash it)

    @field_validator("email")
    @classmethod
    def email_lowercase(cls, v: str) -> str:
        return v.lower()

    # "before" mode: receives raw input (could be string) before type coercion
    @field_validator("created_at", mode="before")
    @classmethod
    def parse_created_at(cls, v):
        if isinstance(v, str):
            return datetime.fromisoformat(v)
        return v


if __name__ == "__main__":
    reg = Registration(
        username="AliceDev",
        email="ALICE@EXAMPLE.COM",
        password="secretpass123",
        created_at="2025-01-15T09:30:00",
    )
    print(reg.username)      # aliceDev  (lowercased)
    print(reg.email)         # alice@example.com  (lowercased)
    print(reg.created_at)    # 2025-01-15 09:30:00  (parsed from string)


# =============================================================================
# SECTION 5: Nested Models — Composition at Scale
# =============================================================================

class Address(BaseModel):
    street: str
    city: str
    country: str = "USA"
    zip_code: str


class Employee(BaseModel):
    id: int
    name: str
    email: str
    address: Address          # nested BaseModel — validated recursively
    manager_id: int | None = None


if __name__ == "__main__":
    emp = Employee(
        id=1,
        name="Dave",
        email="dave@corp.com",
        address={
            "street": "123 Main St",
            "city": "Austin",
            "country": "USA",
            "zip_code": "78701",
        },
    )
    print(emp.address.city)   # Austin
    print(emp.model_dump_json(indent=2))
    # Pydantic serializes the nested Address automatically


# =============================================================================
# SECTION 6: Computed Fields
# =============================================================================
# Fields derived from other fields — no extra data to store.

class Order(BaseModel):
    items: list[str]
    price_per_item: float
    tax_rate: float = 0.08

    @computed_field
    @property
    def subtotal(self) -> float:
        return len(self.items) * self.price_per_item

    @computed_field
    @property
    def tax(self) -> float:
        return self.subtotal * self.tax_rate

    @computed_field
    @property
    def total(self) -> float:
        return self.subtotal + self.tax


if __name__ == "__main__":
    order = Order(items=["Coffee", "Muffin", "Muffin"], price_per_item=3.50)
    print(f"Subtotal: ${order.subtotal:.2f}")  # $10.50
    print(f"Tax:      ${order.tax:.2f}")      # $0.84
    print(f"Total:    ${order.total:.2f}")      # $11.34


# =============================================================================
# SECTION 7: model_config — Behavior Without Inheritance
# =============================================================================
# Configure serialization, validation strictness, aliasing, and more.

class StrictUser(BaseModel):
    model_config = ConfigDict(
        strict=True,        # no automatic type coercion (int("42") fails)
        extra="forbid",      # reject fields not defined in the model
        populate_by_name=True,  # accept both alias and field name on load
    )

    name: str
    age: int


if __name__ == "__main__":
    # strict=True: int("30") is rejected — must pass actual int
    try:
        StrictUser(name="Bob", age="30")  # age is str, not int
    except Exception as e:
        print(f"Strict caught: {e}")

    # extra="forbid": unknown fields are rejected
    try:
        StrictUser(name="Bob", age=30, unknown_field="nope")
    except Exception as e:
        print(f"Extra field caught: {e}")


# =============================================================================
# SECTION 8: Generic Models — Reusable Templates
# =============================================================================

class ApiResponse(BaseModel):
    data: User | None = None
    error: str | None = None
    status_code: int = 200


class PaginatedList(BaseModel):
    items: list[str]
    total: int
    page: int
    page_size: int

    @computed_field
    @property
    def total_pages(self) -> int:
        return (self.total + self.page_size - 1) // self.page_size


if __name__ == "__main__":
    # Use a concrete type for the generic ApiResponse demo
    user_response = ApiResponse(data=user, status_code=200)
    print(user_response.model_dump())

    page = PaginatedList(
        items=["Alice", "Bob", "Carol"],
        total=42,
        page=1,
        page_size=3,
    )
    print(f"Page 1 of {page.total_pages}")  # Page 1 of 14


# =============================================================================
# SECTION 9: Where BaseModel Is Most Used (Real-World Use Cases)
# =============================================================================
# 1. **API request/response schemas** (FastAPI, Flask + Pydantic, Django + Pydantic)
#      FastAPI uses BaseModel for request bodies, query params, and responses.
#      It validates incoming JSON before it ever reaches your handler.
#
# 2. **Configuration objects** — replace ad-hoc dicts and env-var parsing:
#      class Settings(BaseModel):
#          database_url: str
#          secret_key: str
#          debug: bool = False
#      settings = Settings(**os.environ)  # validated on startup
#
# 3. **Data Transfer Objects (DTOs)** — clean boundaries between layers:
#      repository returns DomainModel, converts to UserDTO(BaseModel),
#      which is sent over the API wire.
#
# 4. **Form validation** — validates HTML form data or multipart uploads.
#
# 5. **Event/message schemas** — publish events to message queues with
#      a schema that's enforced at both publisher and consumer sides.


# =============================================================================
# SECTION 10: Why BaseModel Helps Classes and Objects
# =============================================================================
# Traditional Python classes give you structure, but no guarantees:
#
#     class User:
#         def __init__(self, name, email, age):
#             self.name = name          # could be int, could be None, could be ""
#             self.email = email        # could be anything
#             self.age = age            # could be -999
#
#     u = User("", "not-an-email", -5)  # silently accepts garbage
#
# BaseModel adds four things to your classes:
#
#   1. Automatic validation  — data is checked before the object is created.
#   2. Type coercion       — "30" (str) becomes 30 (int) automatically.
#   3. Serialization       — .model_dump() / .model_dump_json() — no __dict__ hacks.
#   4. Documentation       — Field(...) descriptions become OpenAPI schema docs.
#
# It also integrates with:
#   - IDE autocomplete (fields are class attributes with types)
#   - mypy / static type checkers (compatible with check_mode)
#   - FastAPI, Flask, Django, Dramatiq, Celery, and most data pipelines


if __name__ == "__main__":
    print("=== Basic User ===")
    print(user.model_dump())

    print("\n=== Registration with validators ===")
    print(reg.model_dump())

    print("\n=== Nested Employee ===")
    print(emp.model_dump())

    print("\n=== Computed Order totals ===")
    print(f"Subtotal: ${order.subtotal:.2f}")
    print(f"Tax:      ${order.tax:.2f}")
    print(f"Total:    ${order.total:.2f}")

    print("\n=== Generic ApiResponse ===")
    print(resp.model_dump())

    print("\n=== Generic PaginatedList ===")
    print(f"Page 1 of {page.total_pages}")

    print("\n=== Strict config (errors expected) ===")
    try:
        StrictUser(name="Bob", age="30")
    except Exception as e:
        print(f"  strict int coercion: FAILED (as expected)")
    try:
        StrictUser(name="Bob", age=30, unknown_field="nope")
    except Exception as e:
        print(f"  extra field forbid: FAILED (as expected)")
