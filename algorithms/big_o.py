"""
Algorithm: Big O notation and complexity analysis
"""

# O(1) - Constant
def get_first_element(arr: list):
    return arr[0]  # No matter how large, always one step


# O(log n) - Logarithmic
import math

def binary_search_example(arr: list, target) -> bool:
    """Binary search halves search space each iteration."""
    while len(arr) > 0:
        mid = len(arr) // 2
        if arr[mid] == target:
            return True
        elif arr[mid] < target:
            arr = arr[mid + 1:]
        else:
            arr = arr[:mid]
    return False


# O(n) - Linear
def find_max(arr: list):
    max_val = arr[0]
    for num in arr:
        if num > max_val:
            max_val = num
    return max_val


# O(n log n) - Linearithmic
def merge_sort_complexity(arr: list) -> list:
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort_complexity(arr[:mid])
    right = merge_sort_complexity(arr[mid:])
    return sorted(left + right)  # Timsort is O(n log n)


# O(n²) - Quadratic
def bubble_sort_complexity(arr: list) -> list:
    result = arr.copy()
    n = len(result)
    for i in range(n):
        for j in range(0, n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
    return result


# O(2^n) - Exponential (fibonacci recursive)
def fib_exponential(n: int) -> int:
    if n <= 1:
        return n
    return fib_exponential(n - 1) + fib_exponential(n - 2)


# Common complexity comparison
"""
n=10:
  O(1):     1 operation
  O(log n): 3 operations
  O(n):     10 operations
  O(n log n): 30 operations
  O(n²):    100 operations
  O(2^n):   1024 operations

n=100:
  O(1):     1
  O(log n): 7
  O(n):     100
  O(n log n): 664
  O(n²):    10,000
  O(2^n):   1.27e30 operations (impossible)
"""

print("Complexity classes from fastest to slowest:")
print("1. O(1)       - Constant")
print("2. O(log n)   - Logarithmic")
print("3. O(n)       - Linear")
print("4. O(n log n) - Linearithmic")
print("5. O(n²)      - Quadratic")
print("6. O(2^n)     - Exponential")