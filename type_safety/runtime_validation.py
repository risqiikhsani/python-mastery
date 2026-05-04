"""
Type Safety: Runtime type checking with Pydantic-like validation
"""

from typing import Any, get_origin, get_args, Annotated
from dataclasses import dataclass, field


# Simple validator function
def validate_type(value: Any, expected_type: type) -> bool:
    return isinstance(value, expected_type)


# Custom validator decorator
def validate(field_name: str, validator: Callable[[Any], bool]):
    def decorator(func):
        func._validators = getattr(func, '_validators', [])
        func._validators.append((field_name, validator))
        return func
    return decorator


# Field descriptor
class Field:
    def __init__(self, field_type: type, default=None, description: str = ""):
        self.field_type = field_type
        self.default = default
        self.description = description

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        return getattr(obj, f"_{self.name}", self.default)

    def __set__(self, obj, value):
        if not isinstance(value, self.field_type):
            raise TypeError(
                f"{self.name} must be {self.field_type.__name__}, "
                f"got {type(value).__name__}"
            )
        setattr(obj, f"_{self.name}", value)


# Simple Pydantic-like class
class Model:
    def __init__(self, **data):
        for key, value in data.items():
            setattr(self, key, value)

    @classmethod
    def __init_subclass__(cls):
        # Auto-validate on init
        pass

    def model_validate(cls, data: dict):
        instance = cls.__new__(cls)
        for key, value in data.items():
            setattr(instance, key, value)
        return instance


# Example usage with dataclasses
@dataclass
class User:
    name: str
    age: int
    email: str = field(default="")
    active: bool = True

    def __post_init__(self):
        if not self.name:
            raise ValueError("name cannot be empty")
        if self.age < 0:
            raise ValueError("age cannot be negative")


user = User(name="Alice", age=30)
print(f"User: {user}")

try:
    invalid = User(name="", age=-1)
except ValueError as e:
    print(f"Validation error: {e}")