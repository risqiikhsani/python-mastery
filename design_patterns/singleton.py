"""
Design Patterns: Singleton
"""

# Basic singleton using module (Python's recommended approach)
# Just use a module! It's naturally a singleton.

# Classic singleton with __new__
class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.connection_string = "sqlite:///app.db"
        print(f"Database initialized: {self.connection_string}")

    def query(self, sql: str):
        return f"Executing: {sql}"


db1 = Database()
db2 = Database()
print(f"Same instance? {db1 is db2}")  # True

# Thread-safe singleton with lock
import threading


class ThreadSafeSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance


# Borg pattern (shared state, not same identity)
class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state

    def __repr__(self):
        return f"Borg(state={self._shared_state})"


b1 = Borg()
b2 = Borg()
b1.data = "shared"
print(f"Same state? {b1.data == b2.data}")  # True
print(f"Same object? {b1 is b2}")  # False
print(f"Borg state: {b1}")