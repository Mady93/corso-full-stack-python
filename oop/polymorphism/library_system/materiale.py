"""Base class for library materials
"""

# 2. Classe base
# Attributi comuni: title, code. Comportamento comune: describe().

from .validazioni import testo_valido


class Materiale:
    """Represent a generic library material."""

    def __init__(self, title: str, code: str) -> None:
        """Initialize a material with a title and a code.

        NOTE: this constructor assumes the data is already valid.
        Validation happens BEFORE the object is built, in crea() below
        -- not while building it, and without try/except.
        """
        self.title = title
        self.code = code

    @classmethod
    def crea(cls, title: str, code: str):
        """Factory method: validate the data first, then build the object.

        Returns a Materiale if the data is valid, otherwise None (and an
        error message has already been printed by testo_valido)."""
        if not testo_valido(title, "title"):
            return None
        if not testo_valido(code, "code"):
            return None
        return cls(title, code)

    def describe(self) -> str:
        """Return a basic description of the material.

        # 6. Override
        # Ogni sottoclasse ridefinisce questo metodo: stesso nome,
        # comportamento diverso -> polimorfismo.
        """
        return f"{self.title} [{self.code}]"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(title={self.title!r}, code={self.code!r})"