"""Utilitaria subclass: compact city car, economy segment
"""

# 4. Sottoclasse
# Non aggiunge nuovi campi rispetto a Veicolo (quindi non serve
# ridefinire __init__ né crea(): li eredita così come sono, e `cls`
# nella classmethod crea() li costruisce comunque come Utilitaria).
# Aggiunge però un comportamento specifico: nessun sovrapprezzo.

from typing import override

from .veicolo import Veicolo


class Utilitaria(Veicolo):
    """Represent a compact, economy-segment city car"""

    EMISSIONI_CO2_GKM: int = 120

    # tariffa base, nessun sovrapprezzo
    SOVRAPPREZZO_PERCENTUALE: int = 0

    @override
    def calcola_preventivo(self, giorni: int) -> float | None:
        """Override: no surcharge, keeps the base rental rate"""
        # Nessun sovrapprezzo: usa il calcolo della classe base.
        return super().calcola_preventivo(giorni)

    @override
    def descrivi(self) -> str:
        """Override: specific description for a compact city car"""
        base = super().descrivi()

        # Utilitaria sarebbe Compact car
        return f"Compact car: {base} - {self.EMISSIONI_CO2_GKM} g/km CO2"