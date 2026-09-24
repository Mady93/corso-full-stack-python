"""DVD subclass: part of the library material hierarchy
"""

# 4. Altre sottoclassi
# Caratteristiche distintive: director, duration_minutes.

from .materiale import Materiale
from .validazioni import intero_positivo, testo_valido


class DVD(Materiale):
    """Represent a DVD in the library."""

    def __init__(
        self, title: str, code: str, director: str, duration_minutes: int
    ) -> None:
        """Initialize a DVD. Assumes data was already validated by crea()."""
        # 5. super()
        super().__init__(title, code)
        self.director = director
        self.duration_minutes = duration_minutes

    @classmethod
    def crea(cls, title: str, code: str, director: str, duration_minutes: int):
        """Factory: validates every field, then builds the DVD (or None)."""
        if not testo_valido(title, "title"):
            return None
        if not testo_valido(code, "code"):
            return None
        if not testo_valido(director, "director"):
            return None
        if not intero_positivo(duration_minutes, "duration_minutes"):
            return None
        return cls(title, code, director, duration_minutes)

    def describe(self) -> str:
        """Override: DVD-specific description."""
        return (
            f"DVD: {self.title}, directed by {self.director}, "
            f"{self.duration_minutes} minutes"
        )