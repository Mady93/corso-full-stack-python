# Creazione delle voci di diario.

from .archivio import aggiungi_righe
from .config import FILE_DIARIO
from .eventi import adesso


def nuova_voce():
    testo = input("Scrivi la voce di diario: ").strip()
    if not testo:
        print("Voce vuota: non salvata.")
        return
    aggiungi_righe(FILE_DIARIO, [f"{adesso()} | {testo}"])
    print("Voce salvata.")