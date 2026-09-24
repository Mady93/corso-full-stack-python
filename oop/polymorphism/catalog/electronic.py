"""Electronic subclass: part of the Product class hierarchy"""

from typing import override
from .product import Product


class Electronic(Product):
    def __init__(
        self,
        name: str,
        base_price: float,
        warranty_months: int
    ) -> None:
        # super() richiama il costruttore di Product per inizializzare
        # la parte comune: name e base_price
        super().__init__(name, base_price)

        if warranty_months < 0:
            raise ValueError("Warranty cannot be negative")

        # _warranty_months è lo stato interno della classe
        self._warranty_months = warranty_months

    @property
    def warranty_months(self) -> int:
        # Getter: permette di leggere lo stato interno dall'esterno.
        return self._warranty_months

    @override
    def cost(self) -> float:
        # Il metodo viene ridefinito con il comportamento specifico
        # di Electronic: aliquota standard del 22%
        return round(self.base_price * 1.22, 2)

    @override
    def describe(self) -> str:
        # Il metodo viene ridefinito per descrivere in modo specifico
        # un prodotto elettronico
        return (
            f"Electronic product '{self.name}', "
            f"{self.warranty_months} months warranty"
        )