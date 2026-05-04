"""
OOP: Composition and Aggregation
"""

# Composition - "has-a" relationship, owns its parts
class Engine:
    def __init__(self, horsepower: int):
        self.horsepower = horsepower

    def start(self):
        return f"Engine ({self.horsepower}hp) starting..."


class Car:
    def __init__(self, model: str, horsepower: int):
        self.model = model
        # Composition: Car OWNS the engine
        self._engine = Engine(horsepower)

    def start(self):
        return f"{self.model}: {self._engine.start()}"

    def get_engine_power(self):
        return self._engine.horsepower


# Aggregation - "has-a" relationship, but parts exist independently
class Department:
    def __init__(self, name: str):
        self.name = name
        self._employees = []

    def add_employee(self, employee):
        self._employees.append(employee)

    def list_employees(self):
        return [e.name for e in self._employees]


class Employee:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role


# Composition example
car = Car("Tesla Model 3", 450)
print(car.start())  # Tesla Model 3: Engine (450hp) starting...

# When car is destroyed, engine is destroyed too (composition)


# Aggregation example
eng = Department("Engineering")
alice = Employee("Alice", "Engineer")
bob = Employee("Bob", "Manager")
eng.add_employee(alice)
eng.add_employee(bob)
print(eng.list_employees())  # ['Alice', 'Bob']
# Alice and Bob still exist even if Department is destroyed
# (aggregation - weaker relationship)

print("\nKey difference:")
print("Composition: Car owns Engine (engine dies with car)")
print("Aggregation: Department has Employees (employees live on)")