"""Define the fleet management class
"""

# Ogni operazione rischiosa restituisce True/False/None, stampando un
# messaggio d'errore chiaro. Nessun try/except/raise: il chiamante
# controlla il risultato con un semplice `if`.

from __future__ import annotations

from .noleggio import Noleggio
from .validazioni import intero_non_negativo
from .veicolo import Veicolo


class GestioneFlotta:
    """Manage the vehicle fleet: registration, availability, rentals,
    returns, and ordinary maintenance."""

    def __init__(self) -> None:
        """Initialize an empty fleet"""
        self.veicoli = []
        self.noleggi_attivi = []

    @property
    def veicoli(self) -> list[Veicolo]:
        """Return the registered vehicles"""
        return self._veicoli

    @veicoli.setter
    def veicoli(self, valore: list[Veicolo]) -> None:
        """Set the registered vehicles"""
        # Controllo che venga assegnata una lista
        if isinstance(valore, list):
            self._veicoli = valore

    @property
    def noleggi_attivi(self) -> list[Noleggio]:
        """Return the active rentals"""
        return self._noleggi_attivi

    @noleggi_attivi.setter
    def noleggi_attivi(self, valore: list[Noleggio]) -> None:
        """Set the active rentals"""
        # Controllo che venga assegnata una lista
        if isinstance(valore, list):
            self._noleggi_attivi = valore

    # Registrazione
    def registra_veicolo(self, veicolo: Veicolo) -> bool:
        """Add a vehicle to the fleet. Returns True on success"""
        if not isinstance(veicolo, Veicolo):
            print("[Error] Invalid vehicle")
            return False

        for v in self.veicoli:
            if v.targa == veicolo.targa:
                print(f"[Error] Plate '{veicolo.targa}' is already registered")
                return False

        self.veicoli.append(veicolo)
        return True

    # Consultazione
    def veicoli_disponibili(self) -> list[Veicolo]:
        """Return the list of vehicles currently available for rent"""
        return [v for v in self.veicoli if v.disponibile]

    def veicoli_da_revisionare(self) -> list[Veicolo]:
        """Return the list of vehicles that currently need maintenance"""
        return [v for v in self.veicoli if v.necessita_manutenzione()]

    def cerca_per_targa(self, targa: str) -> Veicolo | None:
        """Return the vehicle with that plate, or None if not found"""
        if not isinstance(targa, str):
            print(
                f"[Error] Plate must be a string, "
                f"received {type(targa).__name__}"
            )
            return None

        targa_norm = targa.upper()

        for v in self.veicoli:
            if v.targa == targa_norm:
                return v

        return None

    # Noleggio
    def noleggia(self, targa: str, giorni: int) -> Noleggio | None:
        """Find a vehicle, check its status, create a rental, and update the fleet"""

        # Controllo che la targa sia una stringa
        if not isinstance(targa, str):
            print(
                f"[Error] Plate must be a string, "
                f"received {type(targa).__name__}"
            )
            return None

        veicolo = self.cerca_per_targa(targa)

        # Nessun veicolo trovato
        if veicolo is None:
            print(f"[Error] No vehicle found with plate '{targa}'")
            return None

        # Veicolo già in noleggio
        if not veicolo.disponibile:
            print(
                f"[Error] Vehicle '{veicolo.targa}' is not available "
                f"(already rented)"
            )
            return None

        # Veicolo che necessita manutenzione
        if veicolo.necessita_manutenzione():
            print(
                f"[Error] Vehicle '{veicolo.targa}' requires maintenance "
                f"before rental"
            )
            return None

        # Calcolo del preventivo
        preventivo = veicolo.calcola_preventivo(giorni)

        if preventivo is None:
            return None

        # Creo il record del noleggio
        noleggio = Noleggio.crea(veicolo, giorni, preventivo)

        if noleggio is None:
            return None

        veicolo.disponibile = False
        self.noleggi_attivi.append(noleggio)

        return noleggio

    # Restituzione
    def restituisci(
        self,
        targa: str,
        km_percorsi: int = 0,
    ) -> Noleggio | None:
        """Close an active rental, update mileage, and make the vehicle available again"""
        if not intero_non_negativo(km_percorsi, "km_percorsi"):
            return None

        targa_norm = targa.upper() if isinstance(targa, str) else targa

        for noleggio in self.noleggi_attivi:
            if noleggio.veicolo.targa == targa_norm:
                noleggio.veicolo.km_totali += km_percorsi
                noleggio.km_percorsi = km_percorsi
                noleggio.veicolo.disponibile = True
                self.noleggi_attivi.remove(noleggio)

                return noleggio

        print(f"[Error] No active rental found for plate '{targa}'")
        return None

    # Manutenzione
    def effettua_manutenzione(self, targa: str) -> bool:
        """Perform ordinary maintenance if the vehicle is not currently rented"""
        veicolo = self.cerca_per_targa(targa)

        # Nessun veicolo trovato
        if veicolo is None:
            print(f"[Error] No vehicle found with plate '{targa}'")
            return False

        # Veicolo attualmente in noleggio
        if not veicolo.disponibile:
            print(
                f"[Error] Vehicle '{veicolo.targa}' is currently rented; "
                f"maintenance cannot be performed"
            )
            return False

        veicolo.effettua_manutenzione()
        return True

    # Stato generale
    def stato_flotta(self) -> str:
        """Return a summary of the current fleet state"""
        disponibili = len(self.veicoli_disponibili())

        return (
            f"Total vehicles: {len(self.veicoli)} | "
            f"Available: {disponibili} | "
            f"Rented: {len(self.veicoli) - disponibili} | "
            f"Active rentals: {len(self.noleggi_attivi)}"
        )