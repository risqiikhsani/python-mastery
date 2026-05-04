"""
Type Safety: Type hints and annotations
"""

from typing import List, Dict, Tuple, Set, Optional, Union, Callable
from typing import Any, TypeVar, Generic, Protocol

# Basic type hints
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Container types
def process_items(items: list[int]) -> dict[str, int]:
    return {"count": len(items), "sum": sum(items)}


# Optional and Union
def find_user(user_id: int) -> Optional[str]:
    return f"User {user_id}" if user_id > 0 else None


def parse_value(value: Union[str, int, float]) -> str:
    return str(value)


# Callable types
def apply(func: Callable[[int], int], value: int) -> int:
    return func(value)


# Generics
T = TypeVar("T")


def first(items: list[T]) -> Optional[T]:
    return items[0] if items else None


# Protocol (structural subtyping)
class Readable(Protocol):
    def read(self) -> str: ...


class File:
    def read(self) -> str:
        return "file content"


def read_all(reader: Readable) -> str:
    return reader.read()


# Type aliases
Vector2D = Tuple[float, float]
Matrix = List[List[float]]

Point = dict[str, float]


def distance(p1: Point, p2: Point) -> float:
    dx = p2["x"] - p1["x"]
    dy = p2["y"] - p1["y"]
    return (dx ** 2 + dy ** 2) ** 0.5


# Usage
print(greet("Alice"))
print(process_items([1, 2, 3]))
print(find_user(1))
print(apply(lambda x: x * 2, 5))
print(distance({"x": 0, "y": 0}, {"x": 3, "y": 4}))  # 5.0