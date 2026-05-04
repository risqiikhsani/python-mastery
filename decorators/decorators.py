"""
Decorators: Function and class decorators
"""

from functools import wraps, lru_cache, cached_property
import time


# Basic decorator
def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper


@log_calls
def add(a, b):
    return a + b


# Decorator with arguments
def repeat(times: int):
    def decorator(func):
        @wraps(func)
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


# Timing decorator
def time_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


# Memoization (built-in)
@lru_cache(maxsize=128)
def expensive_computation(n: int) -> int:
    time.sleep(0.1)
    return n * n


# Class decorator
def add_method(cls):
    def new_method(self):
        return f"Added method on {self}"
    cls.new_method = new_method
    return cls


@add_method
class MyClass:
    pass


# Decorator for validating arguments
def validate_positive(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg < 0:
                raise ValueError(f"Expected positive, got {arg}")
        return func(*args, **kwargs)
    return wrapper


@validate_positive
def divide(a, b):
    return a / b


# Class method decorator
def class_method_debug(method):
    @wraps(method)
    def wrapper(cls, *args, **kwargs):
        print(f"Calling {cls.__name__}.{method.__name__}")
        return method(cls, *args, **kwargs)
    return wrapper


class Math:
    @classmethod
    @class_method_debug
    def add(cls, a, b):
        return a + b


# Usage
print(greet())  # ['Hello!', 'Hello!', 'Hello!']
print(f"Expensive (cached): {expensive_computation(5)}")  # 25 (instant, cached)
obj = MyClass()
print(obj.new_method())
divide(10, 2)  # OK
# divide(-1, 1)  # Raises ValueError