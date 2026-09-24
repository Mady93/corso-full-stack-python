"""Book subclass: part of the library material hierarchy
"""

# 3. Sottoclasse
# Eredita da Materiale, riusa title/code, aggiunge author + pages,
# e ridefinisce describe().

from .materiale import Materiale
from .validazioni import intero_positivo, testo_valido


class Libro(Materiale):
    """Represent a book in the library."""

    def __init__(self, title: str, code: str, author: str, pages: int) -> None:
        """Initialize a book. Assumes data was already validated by crea()."""
        # 5. super() -- riuso l'inizializzazione di Materiale invece di
        # ripetere qui la stessa logica
        super().__init__(title, code)
        self.author = author
        self.pages = pages

    @classmethod
    def crea(cls, title: str, code: str, author: str, pages: int):
        """Factory: validates every field, then builds the Book (or None)."""
        if not testo_valido(title, "title"):
            return None
        if not testo_valido(code, "code"):
            return None
        if not testo_valido(author, "author"):
            return None
        if not intero_positivo(pages, "pages"):
            return None
        return cls(title, code, author, pages)

    def describe(self) -> str:
        """Override: book-specific description."""
        return f"Book: {self.title} by {self.author}, {self.pages} pages"