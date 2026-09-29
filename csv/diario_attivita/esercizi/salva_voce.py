# Esercizio 1 - Prima voce
# Realizza un programma che salvi una voce di diario in un file di testo persistente.
# Concetti: open() in modalità "a" (append), with, write(), "\n", datetime.

import os
from datetime import datetime

# Percorso della cartella dati/ calcolato a partire da QUESTO file:
# così il programma funziona anche se lo lanci da un'altra cartella.
# Questo file sta in esercizi/: la cartella del progetto è quella sopra
CARTELLA_PROGETTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARTELLA_DATI = os.path.join(CARTELLA_PROGETTO, "dati")
FILE_DIARIO = os.path.join(CARTELLA_DATI, "diario.txt")


def main():
    testo = input("Scrivi la voce di diario: ").strip()
    if not testo:
        print("Voce vuota: non salvata.")
        return

    # Data e ora attuali in formato leggibile, es. 2026-09-29 08:15
    data_ora = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Creo la cartella dati/ se non esiste (exist_ok=True: nessun errore se c'è già)
    os.makedirs(CARTELLA_DATI, exist_ok=True)

    # "a" = append: aggiunge in fondo senza cancellare le voci precedenti.
    # Se il file non esiste, viene creato.
    with open(FILE_DIARIO, "a", encoding="utf-8") as file:
        # \n serve per andare a capo: una voce = una riga
        file.write(f"{data_ora} | {testo}\n")

    print("Voce salvata.")


if __name__ == "__main__":
    main()