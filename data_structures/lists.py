"""
Python Lists: creation, indexing, methods
"""

# Creation
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]

# Indexing
print(fruits[0])   # apple
print(fruits[-1])  # cherry

# Slicing
print(numbers[1:4])   # [2, 3, 4]
print(numbers[::2])   # [1, 3, 5]
print(numbers[::-1])  # [5, 4, 3, 2, 1] (reverse)

# Modify
fruits[0] = "apricot"
fruits.append("date")         # add to end
fruits.insert(1, "blueberry") # insert at index
fruits.remove("banana")       # remove by value
popped = fruits.pop()         # remove and return last
print(fruits)

# List operations
a = [1, 2]
b = [3, 4]
c = a + b        # [1, 2, 3, 4]
d = a * 3        # [1, 2, 1, 2, 1, 2]

# List methods
nums = [3, 1, 4, 1, 5, 9, 2, 6]
nums.sort()
print(nums)  # [1, 1, 2, 3, 4, 5, 6, 9]

nums.reverse()
print(nums)  # [9, 6, 5, 4, 3, 2, 1, 1]

print(nums.count(1))  # 2 (occurrences)
print(nums.index(5))  # 2 (first position)

# List comprehension
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
print(f"Squares: {squares}")
print(f"Evens: {evens}")

# Nested lists
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(matrix[1][1])  # 5

# Unpacking
first, *middle, last = [1, 2, 3, 4, 5]
print(first, middle, last)  # 1 [2, 3, 4] 5

# Copy (important!)
original = [1, 2, 3]
shallow_copy = original[:]
deep_copy = original.copy()