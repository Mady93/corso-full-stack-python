"""fleet_system package: the Veicolo hierarchy, Noleggio and GestioneFlotta,
plus shared validation functions (no exceptions are used)"""

from .elettrica import Elettrica
from .gestione_flotta import GestioneFlotta
from .noleggio import Noleggio
from .suv import Suv
from .utilitaria import Utilitaria
from .veicolo import Veicolo

__all__ = [
    "Elettrica",
    "GestioneFlotta",
    "Noleggio",
    "Suv",
    "Utilitaria",
    "Veicolo",
]