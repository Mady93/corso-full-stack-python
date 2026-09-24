"""Define the library loan class"""

from .materiale import Materiale
from .utente import Utente


class Prestito:
    """Represent a loan of a library material to a user."""

    def __init__(self, materiale: Materiale, utente: Utente) -> None:
        """Initialize a loan. Assumes data was already validated by crea()."""
        self.materiale = materiale
        self.utente = utente

    # Questo metodo appartiene alla classe e lavora sulla classe, non sul singolo oggetto
    @classmethod
    def crea(cls, materiale, utente):
        """Factory: checks the types, then builds the Loan (or None).

        A Loan only makes sense between a real Material (or subclass)
        and a real User -- not an arbitrary object.
        """
        if not isinstance(materiale, Materiale):
            print(
                "[Error] Invalid material: must be a Material object "
                "(Book, Magazine, DVD, ...)"
            )
            return None
        if not isinstance(utente, Utente):
            print("[Error] Invalid user: must be a User object")
            return None
        return cls(materiale, utente)

    def describe(self) -> str:
        """Return a description of the loan."""
        return f"Loan: {self.materiale.title} -> {self.utente.name}"

    def __repr__(self) -> str:
        return f"Loan(material={self.materiale.title!r}, user={self.utente.name!r})"