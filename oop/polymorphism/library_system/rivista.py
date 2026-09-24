"""Magazine subclass: part of the library material hierarchy
"""

# 4. Altre sottoclassi
# Caratteristiche distintive: issue_number, month.

from .materiale import Materiale
from .validazioni import intero_positivo, testo_valido


class Rivista(Materiale):
    """Represent a magazine in the library."""

    def __init__(self, title: str, code: str, issue_number: int, month: str) -> None:
        """Initialize a magazine. Assumes data was already validated by crea()."""
        # 5. super()
        super().__init__(title, code)
        self.issue_number = issue_number
        self.month = month

    @classmethod
    def crea(cls, title: str, code: str, issue_number: int, month: str):
        """Factory: validates every field, then builds the Magazine (or None)."""
        if not testo_valido(title, "title"):
            return None
        if not testo_valido(code, "code"):
            return None
        if not intero_positivo(issue_number, "issue_number"):
            return None
        if not testo_valido(month, "month"):
            return None
        return cls(title, code, issue_number, month)

    def describe(self) -> str:
        """Override: magazine-specific description."""
        return f"Magazine: {self.title}, issue {self.issue_number}, {self.month}"