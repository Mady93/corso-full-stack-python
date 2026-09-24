"""Define the library user class
"""

# Utente NON fa parte della gerarchia di Materiale: è un tipo di entità
# diverso, condivide describe() per convenzione, non per ereditarietà.

from .validazioni import intero_non_negativo, testo_valido


class Utente:
    """Represent a registered library user."""

    def __init__(self, name: str, user_id: int) -> None:
        """Initialize a user. Assumes data was already validated by crea()."""
        self.name = name
        self.user_id = user_id

    @classmethod
    def crea(cls, name: str, user_id: int):
        """Factory: validates the data, then builds the User (or None)."""
        if not testo_valido(name, "name"):
            return None
        if not intero_non_negativo(user_id, "user_id"):
            return None
        return cls(name, user_id)

    def describe(self) -> str:
        """Return a description of the user."""
        return f"User: {self.name} (ID: {self.user_id})"

    def __repr__(self) -> str:
        return f"Utente(name={self.name!r}, user_id={self.user_id!r})"