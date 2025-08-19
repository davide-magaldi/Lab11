from dataclasses import dataclass


@dataclass
class Product:
    Product_number: int
    Product: str
    Product_color: str

    def __hash__(self):
        return hash(self.Product_number)


