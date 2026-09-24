"""FoodItem subclass: part of the Product class hierarchy"""

from typing import override
from .product import Product


class FoodItem(Product):
    def __init__(
        self,
        name: str,
        base_price: float,
        expiry_days: int
    ) -> None:
        # super() richiama il costruttore di Product per inizializzare
        # la parte comune: name e base_price
        super().__init__(name, base_price)

        if expiry_days <= 0:
            raise ValueError("Days until expiry must be positive")

        # _expiry_days è lo stato interno della classe.
        self._expiry_days = expiry_days

    @property
    def expiry_days(self) -> int:
        # Getter: permette di leggere lo stato interno dall'esterno
        return self._expiry_days

    @override
    def cost(self) -> float:
        # Il metodo viene ridefinito con il comportamento specifico
        # di FoodItem: aliquota ridotta del 10%
        return round(self.base_price * 1.10, 2)

    @override
    def describe(self) -> str:
        # Il metodo viene ridefinito per descrivere in modo specifico
        # un prodotto alimentare
        return f"Food item '{self.name}', expires in {self.expiry_days} days"