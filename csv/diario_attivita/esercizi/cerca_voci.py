# Esercizio 3 - Ricerca
# Realizza un programma che cerchi e mostri le voci di diario contenenti un testo scelto dall'utente.
# Concetti: operatore "in", lower() per ignorare maiuscole/minuscole.

import os

# Questo file sta in esercizi/: la cartella del progetto è quella sopra
CARTELLA_PROGETTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARTELLA_DATI = os.path.join(CARTELLA_PROGETTO, "dati")
FILE_DIARIO = os.path.join(CARTELLA_DATI, "diario.txt")


def main():
    if not os.path.exists(FILE_DIARIO):
        print("Il diario non esiste ancora: esegui prima salva_voce.py")
        return

    testo = input("Testo da cercare: ").strip().lower()
    if not testo:
        print("Non hai scritto nulla.")
        return

    trovate = 0
    with open(FILE_DIARIO, "r", encoding="utf-8") as file:
        for riga in file:
            riga = riga.strip()
            # Cerco nell'intera riga (quindi anche nella data:
            # scrivendo "2026-09-29" trovo le voci di quel giorno).
            if riga and testo in riga.lower():
                print(riga)
                trovate += 1

    if trovate == 0:
        print("Nessuna voce trovata.")
    else:
        print(f"\n{trovate} voci trovate")


if __name__ == "__main__":
    main()