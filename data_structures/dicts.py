"""
Python Dictionaries: key-value storage
"""

# Creation
person = {"name": "Alice", "age": 30, "city": "NYC"}
empty = {}
pairs = dict([("a", 1), ("b", 2)])  # from list of tuples

# From keyword args
d = dict(name="Bob", age=25)
print(person)

# Access
print(person["name"])      # Alice
# print(person["unknown"])  # KeyError!
print(person.get("unknown", "default"))  # default
print(person.get("age", 0))  # 30

# Add/modify
person["email"] = "alice@example.com"
person["age"] = 31

# Remove
del person["city"]
email = person.pop("email")
print(person)

# Iteration
for key in person:
    print(f"{key}: {person[key]}")

# .items(), .keys(), .values()
for key, value in person.items():
    print(f"{key} = {value}")

# Check keys
print("name" in person)   # True
print("email" in person)  # False

# Update/merge
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
d1.update(d2)
print(d1)  # {'a': 1, 'b': 3, 'c': 4}

# Dictionary comprehension
squares = {x: x**2 for x in range(5)}
print(squares)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Defaultdict - auto-initialize missing keys
from collections import defaultdict
dd = defaultdict(list)
dd["fruits"].append("apple")
dd["fruits"].append("banana")
dd["colors"].append("red")
print(dd)  # {'fruits': ['apple', 'banana'], 'colors': ['red']}

# OrderedDict (Python 3.7+ dicts maintain insertion order)
from collections import OrderedDict