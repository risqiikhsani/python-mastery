"""
Performance: Profiling and benchmarking
"""

import time
from functools import wraps

# Time tracking
def time_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {(end - start) * 1000:.2f}ms")
        return result
    return wrapper


# Benchmark helper
def benchmark(func, *args, iterations=1000, **kwargs):
    start = time.perf_counter()
    for _ in range(iterations):
        func(*args, **kwargs)
    end = time.perf_counter()
    total = (end - start) * 1000
    avg = total / iterations
    print(f"{func.__name__}: {total:.2f}ms total, {avg:.4f}ms avg ({iterations} iterations)")


# Profiling with cProfile
import cProfile
import pstats
from io import StringIO


def slow_function():
    return sum(i * i for i in range(10_000))


def fast_function():
    return sum(i * i for i in range(10_000))


# Compare approaches
@time_it
def append_vs_extend():
    result = []
    for i in range(10_000):
        result.append(i)
    return result


@time_it
def list_comprehension():
    return [i for i in range(10_000)]


# Profile a function
def run_profiler(func):
    profiler = cProfile.Profile()
    profiler.enable()
    func()
    profiler.disable()

    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats("cumulative")
    stats.print_stats(10)
    print(stream.getvalue())


print("=== Timing ===")
append_vs_extend()
list_comprehension()

print("\n=== Profiling ===")
run_profiler(fast_function)