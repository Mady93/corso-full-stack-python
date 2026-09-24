"""Elettrica subclass: electric vehicle, eco-friendly discount
"""

# 4. Sottoclasse
# Caratteristiche distintive: autonomia_km, tempo_ricarica_ore,
# sconto ecologico -10%, soglia di manutenzione più alta (motore
# elettrico, meno parti soggette a usura).

from __future__ import annotations

from typing import override

from .validazioni import (
    intero_non_negativo,
    intero_positivo,
    numero_positivo,
    testo_valido,
)
from .veicolo import Veicolo


class Elettrica(Veicolo):
    """Represent an electric vehicle: zero emissions, rental discount"""

    EMISSIONI_CO2_GKM: int = 0

    # -10%: sconto ecologico
    SOVRAPPREZZO_PERCENTUALE: int = -10

    # motore elettrico, manutenzione meno frequente
    SOGLIA_KM_MANUTENZIONE: int = 20_000

    def __init__(
        self,
        targa: str,
        marca: str,
        modello: str,
        posti: int,
        km_totali: int,
        tariffa_giornaliera_base: float,
        autonomia_km: int,
        tempo_ricarica_ore: float,
    ) -> None:
        """Initialize an electric vehicle"""
        super().__init__(
            targa,
            marca,
            modello,
            posti,
            km_totali,
            tariffa_giornaliera_base,
        )

        self.autonomia_km = autonomia_km
        self.tempo_ricarica_ore = tempo_ricarica_ore

    @property
    def autonomia_km(self) -> int:
        """Return the electric vehicle range in kilometres"""
        return self._autonomia_km

    @autonomia_km.setter
    def autonomia_km(self, valore: int) -> None:
        """Set the electric vehicle range after validation"""
        # Controllo che l'autonomia sia un intero positivo.
        if intero_positivo(valore, "autonomia_km"):
            self._autonomia_km = valore

    @property
    def tempo_ricarica_ore(self) -> float:
        """Return the charging time in hours"""
        return self._tempo_ricarica_ore

    @tempo_ricarica_ore.setter
    def tempo_ricarica_ore(self, valore: float) -> None:
        """Set the charging time after validation"""
        # Controllo che il tempo di ricarica sia un numero positivo
        if numero_positivo(valore, "tempo_ricarica_ore"):
            self._tempo_ricarica_ore = valore

    @classmethod
    def crea(
        cls,
        targa: str,
        marca: str,
        modello: str,
        posti: int,
        km_totali: int,
        tariffa_giornaliera_base: float,
        autonomia_km: int,
        tempo_ricarica_ore: float,
    ) -> Elettrica | None:
        """Validate every field and create an Elettrica object"""

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
        if not intero_positivo(autonomia_km, "autonomia_km"):
            return None
        if not numero_positivo(
            tempo_ricarica_ore,
            "tempo_ricarica_ore",
        ):
            return None

        return cls(
            targa,
            marca,
            modello,
            posti,
            km_totali,
            tariffa_giornaliera_base,
            autonomia_km,
            tempo_ricarica_ore,
        )

    @override
    def calcola_preventivo(self, giorni: int) -> float | None:
        """Apply the eco-friendly discount to the base quote"""

        costo_base = super().calcola_preventivo(giorni)

        if costo_base is None:
            return None

        return round(
            costo_base * (1 + self.SOVRAPPREZZO_PERCENTUALE / 100),
            2,
        )

    @override
    def descrivi(self) -> str:
        """Provide a specific description for an electric vehicle"""

        base = super().descrivi()

        return (
            f"Electric: {base} - range {self.autonomia_km} km - "
            f"charging time {self.tempo_ricarica_ore}h - 0 g/km CO2"
        )