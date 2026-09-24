"""SUV subclass: family vehicle, more seats, extra surcharge"""

# 4. Sottoclasse
# Caratteristiche distintive: trazione_integrale, sovrapprezzo +30%

from __future__ import annotations

from typing import override

from .validazioni import (
    booleano_valido,
    intero_non_negativo,
    intero_positivo,
    numero_positivo,
    testo_valido,
)
from .veicolo import Veicolo


class Suv(Veicolo):
    """Represent an SUV: more seats, higher consumption, higher price"""

    EMISSIONI_CO2_GKM: int = 180

    # +30%: più spazio, più consumo
    SOVRAPPREZZO_PERCENTUALE: int = 30

    def __init__(
        self,
        targa: str,
        marca: str,
        modello: str,
        posti: int,
        km_totali: int,
        tariffa_giornaliera_base: float,
        trazione_integrale: bool,
    ) -> None:
        """Initialize an SUV."""
        # 5. super() -- riuso l'inizializzazione di Veicolo invece di
        # ripetere qui la stessa logica
        super().__init__(
            targa,
            marca,
            modello,
            posti,
            km_totali,
            tariffa_giornaliera_base,
        )
        self.trazione_integrale = trazione_integrale

    @property
    def trazione_integrale(self) -> bool:
        """Return whether the SUV has all-wheel drive"""
        return self._trazione_integrale

    @trazione_integrale.setter
    def trazione_integrale(self, valore: bool) -> None:
        """Set whether the SUV has all-wheel drive"""
        # Controllo che la trazione sia un valore booleano
        if booleano_valido(valore, "trazione_integrale"):
            self._trazione_integrale = valore

    @classmethod
    def crea(
        cls,
        targa: str,
        marca: str,
        modello: str,
        posti: int,
        km_totali: int,
        tariffa_giornaliera_base: float,
        trazione_integrale: bool,
    ) -> "Suv | None":
        """Validate every field and create an SUV object"""
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
        if not booleano_valido(
            trazione_integrale,
            "trazione_integrale",
        ):
            return None

        return cls(
            targa,
            marca,
            modello,
            posti,
            km_totali,
            tariffa_giornaliera_base,
            trazione_integrale,
        )

    @override
    def calcola_preventivo(self, giorni: int) -> float | None:
        """Apply the SUV surcharge to the base quote"""
        costo_base = super().calcola_preventivo(giorni)

        if costo_base is None:
            return None

        return round(
            costo_base * (1 + self.SOVRAPPREZZO_PERCENTUALE / 100),
            2,
        )

    @override
    def descrivi(self) -> str:
        """Provide a specific description for an SUV"""
        base = super().descrivi()

        trazione = "4x4" if self.trazione_integrale else "2WD"

        return (
            f"SUV: {base} - {trazione} - "
            f"{self.EMISSIONI_CO2_GKM} g/km CO2"
        )