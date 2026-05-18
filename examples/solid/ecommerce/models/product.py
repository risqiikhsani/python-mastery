import uuid

class Product:
    def __init__(self, name: str, price: float, description: str = ""):
        self.id = uuid.uuid4().hex
        self.name = name
        self.price = price
        self.description = description