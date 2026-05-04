"""
Algorithm: Sorting algorithms
"""

# Bubble sort - O(n²)
def bubble_sort(arr: list) -> list:
    result = arr.copy()
    n = len(result)
    for i in range(n):
        for j in range(0, n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
    return result


# Selection sort - O(n²), fewer swaps
def selection_sort(arr: list) -> list:
    result = arr.copy()
    n = len(result)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if result[j] < result[min_idx]:
                min_idx = j
        result[i], result[min_idx] = result[min_idx], result[i]
    return result


# Merge sort - O(n log n)
def merge_sort(arr: list) -> list:
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left: list, right: list) -> list:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# Quick sort - O(n log n) average, O(n²) worst
def quick_sort(arr: list) -> list:
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)


# Python built-in (Timsort - O(n log n))
def python_sort(arr: list) -> list:
    return sorted(arr)


# Test
import random
data = [random.randint(0, 100) for _ in range(20)]

print(f"Original: {data[:10]}...")
print(f"Merge:    {merge_sort(data)[:10]}...")
print(f"Quick:    {quick_sort(data)[:10]}...")
print(f"Python:   {python_sort(data)[:10]}...")