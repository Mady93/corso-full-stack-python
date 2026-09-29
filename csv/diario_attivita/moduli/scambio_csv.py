# Esportazione del log in CSV e importazione di attività da CSV.

import csv
import os

from .archivio import aggiungi_righe, leggi_righe
from .config import CAMPI_CSV, CARTELLA_DATI, CSV_DEFAULT, FILE_EXPORT, FILE_LOG
from .eventi import evento_a_riga, leggi_log


def esporta_csv():
    eventi = leggi_log()
    if not eventi:
        print("Il log è vuoto: niente da esportare.")
        return
    # "w": l'export si rigenera da zero (niente duplicati, una sola intestazione)
    with open(FILE_EXPORT, "w", newline="", encoding="utf-8") as file:
        scrittore = csv.DictWriter(file, fieldnames=CAMPI_CSV)
        scrittore.writeheader()
        for numero, e in enumerate(eventi, start=1):
            scrittore.writerow({"id": numero, "data_ora": e["data_ora"],
                                "categoria": e["categoria"],
                                "descrizione": e["descrizione"],
                                "durata_minuti": e["durata"]})
    print(f"Esportati {len(eventi)} eventi in {FILE_EXPORT}")


def importa_csv():
    nome = input(f"File CSV in dati/ [Invio = {CSV_DEFAULT}]: ").strip() or CSV_DEFAULT
    percorso = os.path.join(CARTELLA_DATI, nome)
    try:
        with open(percorso, "r", newline="", encoding="utf-8") as file:
            righe_csv = list(csv.DictReader(file))
    except FileNotFoundError:
        print(f"File non trovato: {percorso}")
        return

    # Per non duplicare le attività, confronto con le righe già presenti nel log
    gia_presenti = set(leggi_righe(FILE_LOG))
    nuove = []
    scartate = 0
    for r in righe_csv:
        durata = str(r.get("durata_minuti", "")).strip()
        if not durata.isdigit() or not r.get("data_ora") or not r.get("descrizione"):
            scartate += 1          # riga incompleta o con durata non valida
            continue
        riga = evento_a_riga({
            "data_ora": r["data_ora"].strip(),
            "categoria": r.get("categoria", "").strip().lower(),
            "descrizione": r["descrizione"].strip().replace("|", "/"),
            "durata": int(durata),
        })
        if riga not in gia_presenti:
            nuove.append(riga)
            gia_presenti.add(riga)

    aggiungi_righe(FILE_LOG, nuove)
    doppie = len(righe_csv) - len(nuove) - scartate
    print(f"Importate {len(nuove)} attività nuove "
          f"({doppie} già presenti, {scartate} scartate).")