"""
Error Handling: Exceptions and custom errors
"""

# Built-in exceptions hierarchy
# BaseException
#   ├── SystemExit
#   ├── KeyboardInterrupt
#   └── Exception
#       ├── StopIteration
#       ├── ArithmeticError
#       │   ├── FloatingPointError
#       │   ├── OverflowError
#       │   └── ZeroDivisionError
#       ├── LookupError
#       │   ├── IndexError
#       │   └── KeyError
#       ├── OSError (IOError)
#       └── ...

# Basic try/except
def divide(a: float, b: float) -> float:
    try:
        return a / b
    except ZeroDivisionError:
        print("Cannot divide by zero!")
        return float('inf')


# Multiple exceptions
def parse_number(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"'{value}' is not a valid number")
    except TypeError:
        raise TypeError(f"Expected string, got {type(value).__name__}")


# Catch multiple exceptions
def process(data):
    try:
        return int(data)
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
        return None


# else clause (runs if no exception)
def safe_divide(a: float, b: float) -> float | None:
    try:
        result = a / b
    except ZeroDivisionError:
        return None
    else:
        print("Division successful!")
        return result


# finally clause (always runs)
def read_file_robust(path: str) -> str | None:
    file = None
    try:
        file = open(path, 'r')
        return file.read()
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None
    finally:
        if file:
            file.close()


# Custom exception
class ValidationError(Exception):
    """Raised when data validation fails."""

    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")


class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def validate(self):
        errors = []
        if not self.name:
            errors.append(ValidationError("name", "cannot be empty"))
        if self.age < 0:
            errors.append(ValidationError("age", "cannot be negative"))
        if errors:
            raise ValidationError("user", f"Validation failed: {errors}")


# Raising exceptions
def validate_age(age: int):
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 150:
        raise ValueError("Age seems unrealistic")


print(divide(10, 0))
try:
    parse_number("not a number")
except ValueError as e:
    print(f"Caught: {e}")