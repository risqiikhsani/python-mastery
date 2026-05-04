"""
Algorithm: Recursive functions and memoization
"""

# Simple recursion
def countdown(n: int):
    if n <= 0:
        print("Done!")
        return
    print(n)
    countdown(n - 1)

countdown(5)

# Fibonacci with recursion (naive - exponential time)
def fib_recursive(n: int) -> int:
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)

# Fibonacci with memoization (dynamic programming top-down)
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_memoized(n: int) -> int:
    if n <= 1:
        return n
    return fib_memoized(n - 1) + fib_memoized(n - 2)

# Fibonacci with tabulation (bottom-up dynamic programming)
def fib_tabulation(n: int) -> int:
    if n <= 1:
        return n
    dp = [0, 1] + [0] * (n - 1)
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

# Space-optimized bottom-up
def fib_optimized(n: int) -> int:
    if n <= 1:
        return n
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr

# Comparison
import time

for n in [10, 20, 30, 35]:
    start = time.time()
    result = fib_memoized(n)
    print(f"fib({n}) = {result} (memoized: {(time.time()-start)*1000:.2f}ms)")

# Recursive binary search
def binary_search(arr: list, target: int, low: int = 0, high: int = None) -> int:
    if high is None:
        high = len(arr) - 1
    if low > high:
        return -1

    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid + 1, high)
    else:
        return binary_search(arr, target, low, mid - 1)

numbers = [1, 3, 5, 7, 9, 11, 13, 15]
print(f"Found 7 at index: {binary_search(numbers, 7)}")  # 3