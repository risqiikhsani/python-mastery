"""
Iterators and Generators: Lazy evaluation
"""

from typing import Iterator, Generator
from itertools import islice, count, cycle, chain, filterfalse


# Iterator protocol
class CountDown:
    def __init__(self, start: int):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1


# Generator function
def count_up(to: int) -> Generator[int, None, None]:
    current = 0
    while current <= to:
        yield current
        current += 1


def fibonacci() -> Generator[int, None, None]:
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


# Generator expression (like list comprehension but lazy)
squares = (x ** 2 for x in range(1000000))  # No computation yet!
print(f"First 5 squares: {next(squares)}, {next(squares)}, {next(squares)}")


# itertools examples
def itertools_demo():
    # islice - finite slice of iterator
    fib = fibonacci()
    first_10 = list(islice(fib, 10))
    print(f"First 10 Fibonacci: {first_10}")

    # count - infinite counter
    counter = count(start=1, step=2)  # 1, 3, 5, 7...
    odds = list(islice(counter, 5))
    print(f"First 5 odds: {odds}")

    # cycle - repeat forever
    cycler = cycle(['A', 'B', 'C'])
    letters = list(islice(cycler, 7))
    print(f"Cycled: {letters}")  # A B C A B C A

    # chain - concatenate iterables
    combined = list(chain([1, 2], [3, 4], [5, 6]))
    print(f"Chained: {combined}")

    # filterfalse - opposite of filter
    numbers = range(10)
    odds = list(filterfalse(lambda x: x % 2 == 0, numbers))
    print(f"Odd numbers: {odds}")


# Pipeline with generators
def process_data(data: list) -> Iterator[int]:
    # Filter positive
    positive = (x for x in data if x > 0)
    # Double values
    doubled = (x * 2 for x in positive)
    # Take first 5
    limited = islice(doubled, 5)
    return list(limited)


# Infinite generator with state
def password_generator(start: int = 1):
    chars = "abcdefghijklmnopqrstuvwxyz"
    for i in count(start):
        yield f"pass{i}"


def running_sum():
    total = 0
    while True:
        value = yield total
        total += value if value is not None else 0


# Send values into generator
def generator_with_send():
    gen = running_sum()
    next(gen)  # Prime the generator
    print(gen.send(10))  # 10
    print(gen.send(20))  # 30
    print(gen.send(5))   # 35


# Usage
print("Count down:", list(CountDown(5)))
print("Count up:", list(count_up(5)))
print("Fibonacci:", list(islice(fibonacci(), 10)))
itertools_demo()
process_data([-1, 2, 3, -5, 4, 0, 6])  # [4, 6, 8, 12]
generator_with_send()