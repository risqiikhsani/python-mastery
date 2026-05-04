"""
Memory Management: Garbage collection and weak references
"""

import gc
import sys


# Reference counting (Python's primary mechanism)
def reference_counting_demo():
    a = [1, 2, 3]  # ref count = 1
    b = a          # ref count = 2
    del a          # ref count = 1
    del b          # ref count = 0, object destroyed
    print("Object destroyed automatically")


# Circular reference problem
class Node:
    def __init__(self, name):
        self.name = name
        self.next = None

    def __repr__(self):
        return f"Node({self.name})"


def circular_reference_demo():
    node1 = Node("first")
    node2 = Node("second")
    node1.next = node2
    node2.next = node1  # Circular reference!

    # Without gc.collect(), these might not be freed immediately
    del node1
    del node2
    gc.collect()  # Force garbage collection


# Weak references (don't prevent garbage collection)
import weakref


def weakref_demo():
    obj = {"data": "important"}
    weak = weakref.ref(obj)

    print(f"Original: {weak()}")
    del obj
    print(f"After delete: {weak()}")  # None - object was collected!


# Cache using weak references
class Cache:
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()

    def get(self, key: str):
        return self._cache.get(key)

    def set(self, key: str, value):
        self._cache[key] = value


# Finalizers (__del__ and __del__ cleanup)
class FileHandle:
    def __init__(self, filename: str):
        self.filename = filename
        self._handle = open(filename, 'w')
        print(f"Opened {filename}")

    def write(self, data: str):
        self._handle.write(data)

    def __del__(self):
        print(f"Closing {self.filename}")
        self._handle.close()


# Memory profiling
def get_memory_info():
    import sys
    # Size of objects
    print(f"Size of int: {sys.getsizeof(42)} bytes")
    print(f"Size of float: {sys.getsizeof(3.14)} bytes")
    print(f"Size of small list: {sys.getsizeof([1, 2])} bytes")
    print(f"Size of dict: {sys.getsizeof({})} bytes")


# Disable garbage collection (dangerous!)
def gc_control():
    gc.disable()  # Disable automatic GC
    # Do critical operations...
    gc.enable()   # Re-enable
    gc.collect()  # Manual collection