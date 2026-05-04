"""
OOP: Classes and Objects
"""

class Dog:
    # Class attribute (shared by all instances)
    species = "Canis familiaris"

    # Initializer
    def __init__(self, name: str, age: int):
        self.name = name  # instance attribute
        self.age = age

    # Instance method
    def bark(self) -> str:
        return f"{self.name} says woof!"

    # String representation
    def __str__(self) -> str:
        return f"Dog(name={self.name}, age={self.age})"

    # For debugging (more detailed than __str__)
    def __repr__(self) -> str:
        return f"Dog(name={self.name!r}, age={self.age!r})"

    # Instance method with @property
    def speak(self) -> str:
        sounds = {"small": "yip", "medium": "bark", "large": "woof"}
        size = "small" if self.age < 3 else "medium" if self.age < 7 else "large"
        return f"{self.name} says {sounds[size]}!"


# Create instances
rex = Dog("Rex", 5)
buddy = Dog("Buddy", 2)

print(Dog.species)       # Canis familiaris
print(rex.name)         # Rex
print(rex.bark())       # Rex says woof!
print(rex.speak())      # Rex says bark!
print(rex)              # Dog(name=Rex, age=5)
print(repr(rex))        # Dog(name='Rex', age=5)