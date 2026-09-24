"""Book subclass: part of the Product class hierarchy."""

from typing import override
from .product import Product


class Book(Product):
    def __init__(
        self,
        name: str,
        base_price: float,
        author: str,
        pages: int
    ) -> None:
        # super() richiama il costruttore di Product per inizializzare
        # la parte comune: name e base_price
        super().__init__(name, base_price)

        if pages <= 0:
            raise ValueError("Number of pages must be positive")

        # _author e _pages sono lo stato interno specifico di Book.
        self._author = author
        self._pages = pages

    # API pubblica che permette di leggere lo stato interno senza modificarlo
    @property
    def author(self) -> str:
        # Getter: permette di leggere l'autore dall'esterno
        return self._author

    @property
    def pages(self) -> int:
        # Getter: permette di leggere il numero di pagine dall'esterno
        return self._pages

    @override
    def cost(self) -> float:
        # Ridefinisco cost() per Book: i libri hanno un'aliquota del 4%
        return round(self.base_price * 1.04, 2)

    @override
    def describe(self) -> str:
        # Ridefinisco describe() per creare una descrizione specifica del libro
        return f"Book '{self.name}' by {self.author}, {self.pages} pages"

    @override
    def __repr__(self) -> str:
        # Ridefinisco __repr__ per mostrare anche autore e pagine
        return f"Book(name={self.name!r}, author={self.author!r}, pages={self.pages})"