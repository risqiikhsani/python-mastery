"""
Functional Programming: Higher-order functions and closures
"""

from typing import Callable, Iterable, TypeVar

T = TypeVar("T")


# Higher-order function (takes/returns functions)
def apply_twice(func: Callable[[int], int], value: int) -> int:
    """Apply a function twice."""
    return func(func(value))


def add_five(x: int) -> int:
    return x + 5


print(apply_twice(add_five, 1))  # 11 (1+5=6, 6+5=11)


# Closure: function that captures environment
def make_multiplier(factor: float) -> Callable[[float], float]:
    """Factory function that creates multipliers."""
    def multiplier(x: float) -> float:
        return x * factor
    return multiplier


double = make_multiplier(2)
triple = make_multiplier(3)
print(f"Double 5: {double(5)}")  # 10
print(f"Triple 5: {triple(5)}")  # 15


# Currying: transform multi-arg function into chain of single-arg functions
def curried_add(x: int) -> Callable[[int], int]:
    def inner(y: int) -> int:
        return x + y
    return inner


add_five_curried = curried_add(5)
print(f"Curried add 5 to 3: {add_five_curried(3)}")  # 8


# Decorator factory
def repeat(times: int):
    """Decorator that repeats a function call."""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator


@repeat(3)
def greet():
    return "Hello!"


print(greet())  # ['Hello!', 'Hello!', 'Hello!']


# Lazy evaluation with generators
def lazy_map(func: Callable, iterable: Iterable) -> map:
    return map(func, iterable)


# Pipe operator (functional style)
def pipe(value: T, *funcs: Callable) -> T:
    """Pipe value through a series of functions."""
    result = value
    for func in funcs:
        result = func(result)
    return result


result = pipe(
    5,
    lambda x: x * 2,      # 10
    lambda x: x + 3,      # 13
    lambda x: x ** 2,     # 169
)
print(f"Piped result: {result}")