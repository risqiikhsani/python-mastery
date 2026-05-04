"""
Metaprogramming: Metaclasses
"""

# Basic metaclass
class Meta(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        # Automatically register class
        print(f"Creating class: {name}")
        return cls


class MyClass(metaclass=Meta):
    pass


# Entity metaclass - auto-assign IDs
class EntityMeta(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        cls._next_id = 0
        return cls

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        instance.id = cls._next_id
        cls._next_id += 1
        return instance


class Entity(metaclass=EntityMeta):
    pass


class User(Entity):
    def __init__(self, name: str):
        self.name = name


# Singleton metaclass
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    pass


class Database(metaclass=SingletonMeta):
    pass


# Attribute tracking metaclass
class AutoPublishMeta(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)

        # Publish all public methods
        cls.public_methods = [
            attr for attr in dir(cls)
            if not attr.startswith('_') and callable(getattr(cls, attr))
        ]
        return cls


class Service(metaclass=AutoPublishMeta):
    def public_method(self):
        pass

    def _private_method(self):
        pass

    def another_public(self):
        pass


# Usage
user1 = User("Alice")
user2 = User("Bob")
print(f"User1 ID: {user1.id}, User2 ID: {user2.id}")  # 0, 1

db1 = Database()
db2 = Database()
print(f"Same instance? {db1 is db2}")  # True

print(f"Public methods: {Service.public_methods}")