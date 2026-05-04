"""
OOP: Special Methods (__dunder__ methods)
"""

class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    # Arithmetic operators
    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector":
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Vector":
        return self.__mul__(scalar)

    def __matmul__(self, other: "Vector") -> float:
        """Dot product."""
        return self.x * other.x + self.y * other.y

    # Comparison operators
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    # Unary operators
    def __neg__(self) -> "Vector":
        return Vector(-self.x, -self.y)

    def __abs__(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    # String representations
    def __str__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Vector({self.x!r}, {self.y!r})"

    # Callable
    def __call__(self) -> tuple:
        """Make Vector callable like a function."""
        return (self.x, self.y)

    # Length
    def __len__(self) -> int:
        return 2

    # Indexing
    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Vector index out of range")


# Usage
v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(v1 + v2)      # Vector(4, 6)
print(v1 - v2)      # Vector(2, 2)
print(v1 * 2)       # Vector(6, 8)
print(3 * v2)       # Vector(3, 6)
print(v1 @ v2)      # 11 (dot product)
print(-v1)          # Vector(-3, -4)
print(abs(v1))      # 5.0
print(v1())         # (3, 4)
print(v1[0], v1[1]) # 3 4
print(v1 == Vector(3, 4))  # True
print(v1 == "not a vector")  # False