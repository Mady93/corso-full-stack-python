# Esercizio 2 - Consultazione
# Realizza un programma che visualizzi tutte le voci presenti in un diario testuale.
# Concetti: open() in modalità "r", lettura riga per riga, strip(), file inesistente.

import os

# Questo file sta in esercizi/: la cartella del progetto è quella sopra
CARTELLA_PROGETTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARTELLA_DATI = os.path.join(CARTELLA_PROGETTO, "dati")
FILE_DIARIO = os.path.join(CARTELLA_DATI, "diario.txt")


def main():
    # In modalità "r" il file deve esistere: se non c'è, lo segnalo
    # invece di far crashare il programma con FileNotFoundError.
    if not os.path.exists(FILE_DIARIO):
        print("Il diario non esiste ancora: esegui prima salva_voce.py")
        return

    numero = 0
    with open(FILE_DIARIO, "r", encoding="utf-8") as file:
        # Un oggetto file si può scorrere con for: una riga alla volta
        for riga in file:
            riga = riga.strip()      # tolgo lo \n finale
            if riga:                 # salto le righe vuote
                numero += 1
                print(f"{numero:>3}. {riga}")

    if numero == 0:
        print("Il diario è vuoto.")
    else:
        print(f"\nTotale: {numero} voci")


if __name__ == "__main__":
    main()