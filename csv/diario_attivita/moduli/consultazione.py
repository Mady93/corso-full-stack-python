# Consultazione e ricerca su diario e log.

from .archivio import leggi_righe
from .config import FILE_DIARIO, FILE_LOG


def _mostra(percorso, nome):
    # Il _ iniziale indica che la funzione è per uso interno del modulo
    righe = leggi_righe(percorso)
    if not righe:
        print(f"{nome} vuoto o inesistente.")
        return
    for numero, riga in enumerate(righe, start=1):
        print(f"{numero:>3}. {riga}")
    print(f"\nTotale: {len(righe)}")


def consulta_diario():
    _mostra(FILE_DIARIO, "Diario")


def consulta_log():
    _mostra(FILE_LOG, "Log")


def cerca():
    print("Cerca in: 1) Diario  2) Log")
    scelta = input("Scelta: ").strip()
    if scelta == "1":
        righe = leggi_righe(FILE_DIARIO)
    elif scelta == "2":
        righe = leggi_righe(FILE_LOG)
    else:
        print("Scelta non valida.")
        return

    testo = input("Testo da cercare: ").strip().lower()
    if not testo:
        print("Non hai scritto nulla.")
        return
    trovate = [r for r in righe if testo in r.lower()]
    if not trovate:
        print("Nessun risultato.")
        return
    for riga in trovate:
        print(riga)
    print(f"\n{len(trovate)} risultati")