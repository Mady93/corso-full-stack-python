# Esercizio 4 - Log personale
# Realizza un sistema che registri attività con timestamp in un file di log.
# Formato di ogni riga:  data ora | categoria | descrizione | durata in minuti
# Concetti: append, datetime.now(), strftime(), validazione dell'input.

import os
from datetime import datetime

# Questo file sta in esercizi/: la cartella del progetto è quella sopra
CARTELLA_PROGETTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARTELLA_DATI = os.path.join(CARTELLA_PROGETTO, "dati")
FILE_LOG = os.path.join(CARTELLA_DATI, "attivita.log")


def main():
    categoria = input("Categoria (es. studio, sviluppo, pausa): ").strip().lower()
    descrizione = input("Descrizione: ").strip()

    if not categoria or not descrizione:
        print("Categoria e descrizione sono obbligatorie.")
        return

    # Il carattere | è il separatore dei campi: lo tolgo dal testo scritto
    # dall'utente, altrimenti la riga non si potrebbe più dividere correttamente.
    categoria = categoria.replace("|", "/")
    descrizione = descrizione.replace("|", "/")

    # Chiedo la durata finché non è un numero intero
    durata = input("Durata in minuti: ").strip()
    while not durata.isdigit():
        durata = input("Inserisci un numero intero di minuti: ").strip()

    # Il timestamp lo genera il programma, non l'utente
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    os.makedirs(CARTELLA_DATI, exist_ok=True)
    with open(FILE_LOG, "a", encoding="utf-8") as file:
        file.write(f"{timestamp} | {categoria} | {descrizione} | {durata}\n")

    print("Attività registrata.")


if __name__ == "__main__":
    main()