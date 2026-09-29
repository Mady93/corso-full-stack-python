# Esercizio 7 - Importazione CSV
# Realizza un programma che importi voci di diario o attività da un file CSV e le renda consultabili.
# Concetti: csv.DictReader, conversione dei tipi (int), try/except.

import csv
import os

# Questo file sta in esercizi/: la cartella del progetto è quella sopra
CARTELLA_PROGETTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARTELLA_DATI = os.path.join(CARTELLA_PROGETTO, "dati")
FILE_CSV = os.path.join(CARTELLA_DATI, "attivita_esempio.csv")


def importa_attivita():
    """Legge il CSV e restituisce una lista di dizionari."""
    try:
        with open(FILE_CSV, "r", newline="", encoding="utf-8") as file:
            attivita = list(csv.DictReader(file))
    except FileNotFoundError:
        print(f"File non trovato: {FILE_CSV}")
        return []

    # Il CSV restituisce tutto come stringa: id e durata servono come numeri.
    # Le righe incomplete o con id/durata non numerici vengono scartate
    # invece di bloccare il programma con un ValueError.
    valide = []
    for a in attivita:
        completa = all(a.get(campo) for campo in ("data_ora", "categoria", "descrizione"))
        numeri_ok = (str(a.get("id", "")).strip().isdigit()
                     and str(a.get("durata_minuti", "")).strip().isdigit())
        if completa and numeri_ok:
            a["id"] = int(a["id"])
            a["durata_minuti"] = int(a["durata_minuti"])
            valide.append(a)

    scartate = len(attivita) - len(valide)
    if scartate:
        print(f"Attenzione: {scartate} righe scartate perché non valide.")
    return valide


def stampa_tabella(attivita):
    print(f"\n{'ID':<4} {'DATA E ORA':<16} {'CATEGORIA':<10} "
          f"{'DESCRIZIONE':<36} {'MIN':>4}")
    print("-" * 74)
    for a in attivita:
        print(f"{a['id']:<4} {a['data_ora']:<16} {a['categoria']:<10} "
              f"{a['descrizione']:<36} {a['durata_minuti']:>4}")
    print(f"\n{len(attivita)} attività")


def filtra_categoria(attivita):
    categoria = input("Categoria (es. studio, sviluppo): ").strip().lower()
    trovate = [a for a in attivita if a["categoria"].lower() == categoria]
    if trovate:
        stampa_tabella(trovate)
    else:
        print("Nessuna attività in questa categoria.")


def cerca_descrizione(attivita):
    testo = input("Testo da cercare nella descrizione: ").strip().lower()
    trovate = [a for a in attivita if testo in a["descrizione"].lower()]
    if trovate:
        stampa_tabella(trovate)
    else:
        print("Nessuna attività trovata.")


def main():
    attivita = importa_attivita()
    if not attivita:
        return
    print(f"Importate {len(attivita)} attività.")

    while True:
        print("\n=== CONSULTA ATTIVITÀ ===")
        print("1) Visualizza tutte")
        print("2) Filtra per categoria")
        print("3) Cerca nella descrizione")
        print("0) Esci")
        scelta = input("Scelta: ").strip()

        if scelta == "1":
            stampa_tabella(attivita)
        elif scelta == "2":
            filtra_categoria(attivita)
        elif scelta == "3":
            cerca_descrizione(attivita)
        elif scelta == "0":
            print("Arrivederci!")
            break
        else:
            print("Scelta non valida.")


if __name__ == "__main__":
    main()