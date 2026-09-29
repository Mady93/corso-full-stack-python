# Lettura e scrittura dei file di testo (diario e log).
# Gli altri moduli passano da qui, così la gestione dei file è in un solo posto.

import os

from .config import CARTELLA_DATI


def leggi_righe(percorso):
    """Righe di un file come lista di stringhe. Lista vuota se il file non esiste."""
    if not os.path.exists(percorso):
        return []
    with open(percorso, "r", encoding="utf-8") as file:
        return [riga.strip() for riga in file if riga.strip()]


def aggiungi_righe(percorso, righe):
    """Aggiunge una o più righe in fondo al file (append)."""
    os.makedirs(CARTELLA_DATI, exist_ok=True)
    with open(percorso, "a", encoding="utf-8") as file:
        for riga in righe:
            file.write(riga + "\n")