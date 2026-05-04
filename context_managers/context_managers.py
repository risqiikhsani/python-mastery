"""
Context Managers: with statement and resource management
"""

from contextlib import contextmanager, suppress


# Class-based context manager
class FileManager:
    def __init__(self, filename: str, mode: str = 'r'):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        # Return True to suppress exceptions
        return False


# Using context manager
with FileManager('test.txt', 'w') as f:
    f.write("Hello, context!")


# Function-based context manager with contextlib
@contextmanager
def managed_resource(name: str):
    print(f"Acquiring {name}")
    resource = f"Resource({name})"
    try:
        yield resource
    finally:
        print(f"Releasing {name}")


with managed_resource("DB") as res:
    print(f"Using {res}")


# Suppress exceptions
def suppress_demo():
    with suppress(FileNotFoundError, PermissionError):
        with open('nonexistent.txt') as f:
            return f.read()
    return None  # Returns None if file not found


# Redirect stdout temporarily
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO


def redirect_demo():
    buffer = StringIO()
    with redirect_stdout(buffer):
        print("This goes to buffer")
    return buffer.getvalue()


# Timing context manager
from time import perf_counter


@contextmanager
def timer():
    start = perf_counter()
    yield lambda: perf_counter() - start


with timer() as elapsed:
    total = sum(range(1000000))
print(f"Elapsed: {elapsed():.4f}s")


# Exit stack for multiple resources
from contextlib import ExitStack


def exit_stack_demo():
    resources = []
    with ExitStack() as stack:
        for i in range(3):
            f = open(f'temp_{i}.txt', 'w')
            stack.enter_context(f)
            resources.append(f)
            f.write(f"File {i}")

        # All files closed automatically when block exits
    print("All files closed")


# closing() for objects with close() method
from contextlib import closing


class DatabaseConnection:
    def close(self):
        print("Closing database connection")


with closing(DatabaseConnection()) as conn:
    print("Using database connection")
# Automatically calls conn.close()