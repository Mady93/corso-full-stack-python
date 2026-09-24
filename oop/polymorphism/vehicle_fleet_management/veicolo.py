"""Base class for fleet vehicles
"""

# 2. Classe base
# Attributi comuni: targa, marca, modello, posti, km_totali, tariffa.
# Comportamenti comuni: calcola_preventivo(), necessita_manutenzione(),
# effettua_manutenzione(), descrivi().

from __future__ import annotations

import datetime

from .validazioni import (
    booleano_valido,
    intero_non_negativo,
    intero_positivo,
    numero_positivo,
    testo_valido,
)


class Veicolo:
    """Represent a generic vehicle in the fleet."""

    # Soglie di manutenzione ordinaria (attributi di classe). Le
    # sottoclassi possono sovrascriverle: è polimorfismo anche questo,
    # senza bisogno di ridefinire il metodo che le usa.
    SOGLIA_KM_MANUTENZIONE: int = 10_000
    SOGLIA_GIORNI_MANUTENZIONE: int = 180

    def __init__(
        self,
        targa: str,
        marca: str,
        modello: str,
        posti: int,
        km_totali: int,
        tariffa_giornaliera_base: float,
    ) -> None:
        """Initialize a vehicle."""
        self.targa: str = targa.upper()
        self.marca: str = marca
        self.modello: str = modello
        self.posti: int = posti
        self.km_totali: int = km_totali
        self.tariffa_giornaliera_base: float = tariffa_giornaliera_base

        self.disponibile: bool = True

        # Il veicolo "appena registrato" è considerato appena
        # revisionato: la manutenzione parte da qui.
        self.km_ultima_manutenzione: int = km_totali
        self.data_ultima_manutenzione: datetime.date = datetime.date.today()

    @property
    def targa(self) -> str:
        """Return the vehicle plate"""
        return self._targa

    @targa.setter
    def targa(self, valore: str) -> None:
        """Set the vehicle plate after validation"""
        if testo_valido(valore, "targa"):
            self._targa = valore.upper()

    @property
    def marca(self) -> str:
        """Return the vehicle brand"""
        return self._marca

    @marca.setter
    def marca(self, valore: str) -> None:
        """Set the vehicle brand after validation"""
        if testo_valido(valore, "marca"):
            self._marca = valore

    @property
    def modello(self) -> str:
        """Return the vehicle model"""
        return self._modello

    @modello.setter
    def modello(self, valore: str) -> None:
        """Set the vehicle model after validation"""
        if testo_valido(valore, "modello"):
            self._modello = valore

    @property
    def posti(self) -> int:
        """Return the number of seats"""
        return self._posti

    @posti.setter
    def posti(self, valore: int) -> None:
        """Set the number of seats after validation"""
        if intero_positivo(valore, "posti"):
            self._posti = valore

    @property
    def km_totali(self) -> int:
        """Return the total kilometres of the vehicle"""
        return self._km_totali

    @km_totali.setter
    def km_totali(self, valore: int) -> None:
        """Set the total kilometres after validation"""
        if intero_non_negativo(valore, "km_totali"):
            self._km_totali = valore

    @property
    def tariffa_giornaliera_base(self) -> float:
        """Return the base daily rental rate"""
        return self._tariffa_giornaliera_base

    @tariffa_giornaliera_base.setter
    def tariffa_giornaliera_base(self, valore: float) -> None:
        """Set the base daily rental rate after validation"""
        if numero_positivo(valore, "tariffa_giornaliera_base"):
            self._tariffa_giornaliera_base = valore

    @property
    def disponibile(self) -> bool:
        """Return whether the vehicle is available"""
        return self._disponibile

    @disponibile.setter
    def disponibile(self, valore: bool) -> None:
        """Set the vehicle availability after validation"""
        if booleano_valido(valore, "disponibile"):
            self._disponibile = valore

    @property
    def km_ultima_manutenzione(self) -> int:
        """Return the kilometres recorded at the last maintenance"""
        return self._km_ultima_manutenzione

    @km_ultima_manutenzione.setter
    def km_ultima_manutenzione(self, valore: int) -> None:
        """Set the kilometres recorded at the last maintenance"""
        if intero_non_negativo(valore, "km_ultima_manutenzione"):
            self._km_ultima_manutenzione = valore

    @property
    def data_ultima_manutenzione(self) -> datetime.date:
        """Return the date of the last maintenance"""
        return self._data_ultima_manutenzione

    @data_ultima_manutenzione.setter
    def data_ultima_manutenzione(self, valore: datetime.date) -> None:
        """Set the date of the last maintenance"""
        if isinstance(valore, datetime.date):
            self._data_ultima_manutenzione = valore


    @classmethod
    def crea(
        cls,
        targa: str,
        marca: str,
        modello: str,
        posti: int,
        km_totali: int,
        tariffa_giornaliera_base: float,
    ) -> Veicolo | None:
        """Validate every field and create a Veicolo object"""

        # Grazie a `cls`, se questo metodo viene chiamato come
        # `Utilitaria.crea(...)` costruirà correttamente una Utilitaria
        # (non un Veicolo generico), anche se Utilitaria non ridefinisce
        # crea(): è di nuovo ereditarietà/polymorfismo al lavoro.
        if not testo_valido(targa, "targa"):
            return None
        if not testo_valido(marca, "marca"):
            return None
        if not testo_valido(modello, "modello"):
            return None
        if not intero_positivo(posti, "posti"):
            return None
        if not intero_non_negativo(km_totali, "km_totali"):
            return None
        if not numero_positivo(
            tariffa_giornaliera_base,
            "tariffa_giornaliera_base",
        ):
            return None

        return cls(
            targa,
            marca,
            modello,
            posti,
            km_totali,
            tariffa_giornaliera_base,
        )

    def calcola_preventivo(self, giorni: int) -> float | None:
        """Calculate the rental quote for the specified number of days
        """

        # Personalizzazione del calcolo noleggio
        # Comportamento base: tariffa_giornaliera_base * giorni, con
        # sconto del 10% per noleggi di 7 giorni o più. Le sottoclassi
        # aggiungono il proprio sovrapprezzo/sconto chiamando super().

        if not intero_positivo(giorni, "giorni"):
            return None

        costo = self.tariffa_giornaliera_base * giorni

        # sconto noleggio lungo
        if giorni >= 7:
            costo *= 0.90

        return round(costo, 2)

    def necessita_manutenzione(self) -> bool:
        """Return True if the vehicle requires ordinary maintenance."""
        km_da_ultima = (
            self.km_totali - self.km_ultima_manutenzione
        )
        giorni_da_ultima = (
            datetime.date.today() - self.data_ultima_manutenzione
        ).days

        return (
            km_da_ultima >= self.SOGLIA_KM_MANUTENZIONE
            or giorni_da_ultima >= self.SOGLIA_GIORNI_MANUTENZIONE
        )

    def effettua_manutenzione(self) -> None:
        """Register that ordinary maintenance has just been performed"""
        self.km_ultima_manutenzione = self.km_totali
        self.data_ultima_manutenzione = datetime.date.today()

    def descrivi(self) -> str:
        """Provide the basic description of the vehicle"""

        # 6. Override
        # Ogni sottoclasse ridefinisce questo metodo: stesso nome,
        # risultato diverso -> polimorfismo.
        stato = "available" if self.disponibile else "rented"

        return (
            f"{self.marca} {self.modello} [{self.targa}] - "
            f"{self.posti} seats - {stato}"
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(targa={self.targa!r})"