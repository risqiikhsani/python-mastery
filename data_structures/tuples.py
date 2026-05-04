"""
Python Tuples: immutable sequences
"""

# Creation
point = (3, 4)
colors = ("red", "green", "blue")
single = (42,)          # comma needed for single-element tuple
empty = ()

print(f"Point: {point}, first: {point[0]}")

# Tuple is immutable (can't modify)
# point[0] = 5  # TypeError!

# Unpacking
x, y = point
print(f"x={x}, y={y}")

# Extended unpacking
head, *tail = (1, 2, 3, 4, 5)
print(f"head={head}, tail={tail}")  # head=1, tail=[2, 3, 4, 5]

# Multiple return value (common pattern)
def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers)

mn, mx, sm = get_stats([1, 2, 3, 4, 5])
print(f"min={mn}, max={mx}, sum={sm}")

# Named tuples (like lightweight classes)
from collections import namedtuple
Point3D = namedtuple("Point3D", ["x", "y", "z"])
p = Point3D(1, 2, 3)
print(f"Point: x={p.x}, y={p.y}, z={p.z}")

# Tuple methods
t = (1, 2, 2, 3, 2)
print(t.count(2))  # 3
print(t.index(3))  # 3 (first position)

# Why tuples? Faster than lists, can be dict keys, used for fixed data