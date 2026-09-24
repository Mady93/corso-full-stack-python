"""Define the fleet rental record class
"""

from __future__ import annotations

from .validazioni import (
    intero_non_negativo,
    intero_positivo,
    numero_positivo,
)
from .veicolo import Veicolo


class Noleggio:
    """Represent a rental of a vehicle (active or already closed)"""

    def __init__(
        self,
        veicolo: Veicolo,
        giorni: int,
        preventivo: float,
    ) -> None:
        """Initialize a rental"""

        self.veicolo = veicolo
        self.giorni = giorni
        self.preventivo = preventivo

        # aggiornato alla restituzione
        self.km_percorsi = 0

    @property
    def veicolo(self) -> Veicolo:
        """Return the rented vehicle"""
        return self._veicolo

    @veicolo.setter
    def veicolo(self, valore: Veicolo) -> None:
        """Set the rented vehicle"""
        # Controllo che sia un oggetto Veicolo
        if isinstance(valore, Veicolo):
            self._veicolo = valore

    @property
    def giorni(self) -> int:
        """Return the rental duration."""
        return self._giorni

    @giorni.setter
    def giorni(self, valore: int) -> None:
        """Set the rental duration."""
        # Controllo che i giorni siano un intero positivo
        if intero_positivo(valore, "giorni"):
            self._giorni = valore

    @property
    def preventivo(self) -> float:
        """Return the rental quote"""
        return self._preventivo

    @preventivo.setter
    def preventivo(self, valore: float) -> None:
        """Set the rental quote."""
        # Controllo che il preventivo sia un numero positivo
        if numero_positivo(valore, "preventivo"):
            self._preventivo = valore

    @property
    def km_percorsi(self) -> int:
        """Return the distance travelled"""
        return self._km_percorsi

    @km_percorsi.setter
    def km_percorsi(self, valore: int) -> None:
        """Set the distance travelled."""
        # Controllo che i chilometri non siano negativi
        if intero_non_negativo(valore, "km_percorsi"):
            self._km_percorsi = valore

    @classmethod
    def crea(
        cls,
        veicolo: Veicolo,
        giorni: int,
        preventivo: float,
    ) -> Noleggio | None:
        """Validate the data and create a Noleggio object"""
        if not isinstance(veicolo, Veicolo):
            print("[Error] Invalid vehicle: must be a Veicolo object")
            return None

        if not isinstance(giorni, int) or isinstance(giorni, bool):
            print(
                f"[Error] days must be an integer, "
                f"received {type(giorni).__name__}"
            )
            return None

        if giorni <= 0:
            print("[Error] days must be a positive number (> 0)")
            return None

        if not isinstance(preventivo, (int, float)) or isinstance(preventivo, bool):
            print(
                f"[Error] quote must be a number, "
                f"received {type(preventivo).__name__}"
            )
            return None

        if preventivo <= 0:
            print("[Error] quote must be a positive number (> 0)")
            return None

        return cls(veicolo, giorni, preventivo)

    def descrivi(self) -> str:
        """Return a description of the rental."""
        return (
            f"Rental: {self.veicolo.targa} for {self.giorni} days - "
            f"quote €{self.preventivo:.2f}"
        )

    def __repr__(self) -> str:
        return (
            f"Noleggio("
            f"targa={self.veicolo.targa!r}, "
            f"giorni={self.giorni}, "
            f"preventivo={self.preventivo!r})"
        )