"""
Performance: Optimization techniques
"""

import time

# 1. Use local variables (faster than attribute lookup)
class Slow:
    def process(self, data):
        result = []
        for i in range(len(data)):
            if self.validate(data[i]):
                result.append(self.transform(data[i]))
        return result

    def validate(self, x):
        return x > 0

    def transform(self, x):
        return x * 2


class Fast:
    def process(self, data):
        # Cache method references locally
        validate = self.validate
        transform = self.transform
        result = []
        for x in data:
            if validate(x):
                result.append(transform(x))
        return result

    def validate(self, x):
        return x > 0

    def transform(self, x):
        return x * 2


# 2. Use comprehensions over loops
def sum_squares_loop(n):
    total = 0
    for i in range(n):
        total += i * i
    return total


def sum_squares_comprehension(n):
    return sum(i * i for i in range(n))


# 3. Use itertools for lazy evaluation
import itertools

def filter_and_map_slow():
    data = list(range(1000))
    filtered = [x for x in data if x % 2 == 0]
    doubled = [x * 2 for x in filtered]
    return doubled[:10]


def filter_and_map_fast():
    return list(itertools.islice(
        (x * 2 for x in range(1000) if x % 2 == 0),
        10
    ))


# 4. Use sets for membership testing
def find_common_loop():
    list1 = list(range(10000))
    list2 = list(range(5000, 15000))
    common = []
    for item in list1:
        if item in list2:
            common.append(item)
    return common[:10]


def find_common_set():
    list1 = list(range(10000))
    set2 = set(range(5000, 15000))
    return [x for x in list1 if x in set2][:10]


# 5. Use join for string concatenation
def concat_loop():
    strings = ["a"] * 1000
    result = ""
    for s in strings:
        result += s
    return result


def concat_join():
    strings = ["a"] * 1000
    return "".join(strings)


# Benchmark
n = 10000
start = time.perf_counter()
for _ in range(n):
    find_common_loop()
loop_time = (time.perf_counter() - start) * 1000

start = time.perf_counter()
for _ in range(n):
    find_common_set()
set_time = (time.perf_counter() - start) * 1000

print(f"Loop: {loop_time:.2f}ms, Set: {set_time:.2f}ms")
print(f"Set is {loop_time/set_time:.1f}x faster")