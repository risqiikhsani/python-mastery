"""
OOP: Inheritance and Polymorphism
"""

# Base class
class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        raise NotImplementedError("Subclasses must implement speak()")


# Single inheritance
class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name} says woof!"


class Cat(Animal):
    def speak(self) -> str:
        return f"{self.name} says meow!"


class Robot:
    def speak(self) -> str:
        return "Beep boop"


# Polymorphism - different classes with same interface
def make_them_speak(animals: list):
    for animal in animals:
        print(animal.speak())


dog = Dog("Rex")
cat = Cat("Whiskers")

print(dog.speak())  # Rex says woof!
print(cat.speak())  # Whiskers says meow!

# Works with any object that has speak()
make_them_speak([dog, cat, Robot()])
# Rex says woof!
# Whiskers says meow!
# Beep boop


# Multiple inheritance
class Walkable:
    def walk(self) -> str:
        return "Walking..."


class Flyable:
    def fly(self) -> str:
        return "Flying..."


class Dragon(Walkable, Flyable):
    def speak(self) -> str:
        return "Dragons don't speak, they roar!"


drake = Dragon()
print(drake.walk())  # Walking...
print(drake.fly())   # Flying...!
print(drake.speak())  # Dragons don't speak, they roar!


# Method Resolution Order (MRO)
print(Dragon.__mro__)  # Show inheritance chain