"""
Python Sets: unordered, unique elements
"""

# Creation
primes = {2, 3, 5, 7, 11}
from_list = set([1, 2, 2, 3, 3, 3])
print(from_list)  # {1, 2, 3}

# No duplicates (deduplicate)
numbers = [1, 2, 2, 3, 3, 3, 4, 4, 4]
unique = set(numbers)
print(f"Unique from list: {unique}")

# Set operations
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(f"Union: {a | b}")       # {1, 2, 3, 4, 5, 6}
print(f"Intersection: {a & b}")  # {3, 4}
print(f"Difference: {a - b}")   # {1, 2}
print(f"Symmetric diff: {a ^ b}")  # {1, 2, 5, 6}

# Methods
a.union(b)
a.intersection(b)
a.difference(b)
a.symmetric_difference(b)

# Add/remove
primes.add(13)
primes.remove(2)     # raises KeyError if not found
primes.discard(99)   # no error if not found
popped = primes.pop()  # remove arbitrary element

# Check membership
print(3 in primes)   # True
print(99 in primes)  # False

# Set comprehension
evens = {x for x in range(10) if x % 2 == 0}
print(f"Evens: {evens}")

# Frozen set (immutable)
immutable = frozenset([1, 2, 3])
# immutable.add(4)  # AttributeError!

# Use cases
all_emails = {"a@test.com", "b@test.com", "c@test.com"}
new_signups = {"b@test.com", "d@test.com"}
print(f"Already registered: {all_emails & new_signups}")
print(f"New signups to add: {new_emails_to_add}")