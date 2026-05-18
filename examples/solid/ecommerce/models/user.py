import uuid


class User:
    def __init__(self, name: str, email: str | None = None):
        self.id = uuid.uuid4().hex
        self.name = name
        self.email = email

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"
