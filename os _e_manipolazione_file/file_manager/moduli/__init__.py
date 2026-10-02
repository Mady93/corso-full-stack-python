"""Pacchetto dei moduli del file manager."""

from .analisi import analizza_cartella, stampa_analisi
from .backup import (
    crea_backup,
    crea_backup_interattivo,
    elenca_backup,
    elimina_backup,
    menu_gestione_backup,
    ripristina_backup,
    riepilogo_backup,
    verifica_backup,
)
from .explorer import esplora
from .utilita import (
    chiedi_conferma,
    chiedi_percorso,
    formatta_data,
    formatta_dimensione,
)