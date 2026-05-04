"""
Functional Programming: Pure functions and immutability
"""

from typing import Callable, TypeVar
from functools import reduce

T = TypeVar("T")
R = TypeVar("R")


# Pure function (no side effects, same input = same output)
def add(a: int, b: int) -> int:
    """Pure: no side effects."""
    return a + b


# Impure function (side effects)
counter = 0


def add_with_side_effect(a: int) -> int:
    """Impure: modifies global state."""
    global counter
    counter += 1
    return a + counter


# Using dataclasses for immutable data
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def distance_to(self, other: "Point") -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx ** 2 + dy ** 2) ** 0.5


# Immutable list operations (return new lists)
original = [1, 2, 3]
added = original + [4]  # returns new list
doubled = [x * 2 for x in original]  # comprehension
filtered = list(filter(lambda x: x > 1, original))  # filter

# Map, Filter, Reduce
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Map: transform each element
squared = list(map(lambda x: x ** 2, numbers))

# Filter: keep elements that match
evens = list(filter(lambda x: x % 2 == 0, numbers))

# Reduce: combine all elements into one value
total = reduce(lambda acc, x: acc + x, numbers, 0)
product = reduce(lambda acc, x: acc * x, numbers, 1)

# Compose functions
from functools import partial


def compose(*funcs):
    """Compose functions: compose(f, g)(x) = f(g(x))"""
    def inner(x):
        result = x
        for func in reversed(funcs):
            result = func(result)
        return result
    return inner


# Partial application
def power(base: float, exponent: float) -> float:
    return base ** exponent


square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(f"Square of 5: {square(5)}")  # 25
print(f"Cube of 5: {cube(5)}")  # 125