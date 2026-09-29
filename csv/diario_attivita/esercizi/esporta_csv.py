# Esercizio 6 - Esportazione CSV
# Realizza un programma che trasformi le informazioni di un diario o di un log in un file CSV strutturato.
# Concetti: csv.DictWriter, writeheader(), writerow(), newline="".

import csv
import os

# Questo file sta in esercizi/: la cartella del progetto è quella sopra
CARTELLA_PROGETTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARTELLA_DATI = os.path.join(CARTELLA_PROGETTO, "dati")
FILE_LOG = os.path.join(CARTELLA_DATI, "attivita.log")
FILE_EXPORT = os.path.join(CARTELLA_DATI, "attivita_export.csv")
CAMPI = ["id", "data_ora", "categoria", "descrizione", "durata_minuti"]


def leggi_log():
    if not os.path.exists(FILE_LOG):
        return []
    eventi = []
    with open(FILE_LOG, "r", encoding="utf-8") as file:
        for riga in file:
            campi = [c.strip() for c in riga.strip().split("|")]
            if len(campi) == 4 and campi[3].isdigit():
                eventi.append(campi)
    return eventi


def main():
    eventi = leggi_log()
    if not eventi:
        print("Log mancante o vuoto: esegui prima registra_attivita.py")
        return

    # Modalità "w": l'export viene rigenerato da zero a ogni esecuzione,
    # quindi non ci sono righe duplicate e l'intestazione si scrive una volta sola.
    with open(FILE_EXPORT, "w", newline="", encoding="utf-8") as file:
        scrittore = csv.DictWriter(file, fieldnames=CAMPI)
        scrittore.writeheader()
        # Il log non ha un id: lo genero numerando gli eventi da 1
        for numero, (data_ora, categoria, descrizione, durata) in enumerate(eventi, start=1):
            scrittore.writerow({
                "id": numero,
                "data_ora": data_ora,
                "categoria": categoria,
                "descrizione": descrizione,
                "durata_minuti": durata,
            })

    print(f"Esportati {len(eventi)} eventi in {FILE_EXPORT}")


if __name__ == "__main__":
    main()