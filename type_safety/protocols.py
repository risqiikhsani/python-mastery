"""
Type Safety: Protocols for duck typing
"""

from typing import Protocol, runtime_checkable


# Structural typing with Protocol
@runtime_checkable
class Readable(Protocol):
    def read(self, n: int = -1) -> str: ...


@runtime_checkable
class Writable(Protocol):
    def write(self, data: str) -> int: ...


# Implementation 1: File
class File:
    def __init__(self, path: str):
        self.path = path

    def read(self, n: int = -1) -> str:
        with open(self.path) as f:
            return f.read(n)

    def write(self, data: str) -> int:
        with open(self.path, "w") as f:
            return f.write(data)


# Implementation 2: StringIO (in-memory)
from io import StringIO


class StringBuffer:
    def __init__(self):
        self._buffer = StringIO()

    def read(self, n: int = -1) -> str:
        return self._buffer.read(n)

    def write(self, data: str) -> int:
        return self._buffer.write(data)


# Function using protocols (duck typing)
def copy(source: Readable, dest: Writable) -> int:
    """Copy data from source to destination."""
    data = source.read()
    return dest.write(data)


# Test
file_buffer = StringBuffer()
string_io = StringIO()

# Both satisfy the protocol
print(f"File is Readable: {isinstance(file_buffer, Readable)}")  # True
print(f"StringIO is Readable: {isinstance(string_io, Readable)}")  # True

# Use in function
string_io.write("Hello, Protocol!")
file_buffer.write("Copied: ")
copy(string_io, file_buffer)
print(f"Result: {file_buffer.read()}")  # Copied: Hello, Protocol!