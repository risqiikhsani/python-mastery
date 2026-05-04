"""
OOP: Abstraction - abstract classes and methods
"""

from abc import ABC, abstractmethod


class Shape(ABC):
    """Abstract base class for shapes."""

    @abstractmethod
    def area(self) -> float:
        """Calculate the area of the shape."""
        pass

    @abstractmethod
    def perimeter(self) -> float:
        """Calculate the perimeter of the shape."""
        pass

    def describe(self) -> str:
        """Concrete method - shared by all subclasses."""
        return f"This shape has area {self.area():.2f} and perimeter {self.perimeter():.2f}"


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        import math
        return 2 * math.pi * self.radius


# Can't instantiate abstract class
# shape = Shape()  # TypeError!

rect = Rectangle(4, 5)
circle = Circle(3)

print(f"Rectangle area: {rect.area()}")           # 20
print(f"Rectangle perimeter: {rect.perimeter()}")  # 18
print(rect.describe())

print(f"Circle area: {circle.area():.2f}")           # 28.27
print(f"Circle perimeter: {circle.perimeter():.2f}")  # 18.85
print(circle.describe())