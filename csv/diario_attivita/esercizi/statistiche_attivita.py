# Esercizio 8 - Statistiche attività
# Realizza un programma che produca statistiche significative a partire da un file CSV di attività.
# Concetti: sum(), max() con key, dizionari come contatori, sorted().

import csv
import os

# Questo file sta in esercizi/: la cartella del progetto è quella sopra
CARTELLA_PROGETTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARTELLA_DATI = os.path.join(CARTELLA_PROGETTO, "dati")
FILE_CSV = os.path.join(CARTELLA_DATI, "attivita_esempio.csv")


def importa_attivita():
    try:
        with open(FILE_CSV, "r", newline="", encoding="utf-8") as file:
            attivita = list(csv.DictReader(file))
    except FileNotFoundError:
        print(f"File non trovato: {FILE_CSV}")
        return []
    
    # Tengo solo le righe complete e con durata numerica: una riga sporca
    # viene scartata invece di bloccare il programma con un ValueError.
    valide = []
    for a in attivita:
        completa = all(a.get(campo) for campo in ("data_ora", "categoria", "descrizione"))
        if completa and str(a.get("durata_minuti", "")).strip().isdigit():
            a["durata_minuti"] = int(a["durata_minuti"])
            valide.append(a)

    scartate = len(attivita) - len(valide)
    if scartate:
        print(f"Attenzione: {scartate} righe scartate perché non valide.\n")
    return valide


def formatta_durata(minuti):
    # // = divisione intera (ore), % = resto (minuti rimasti). 290 -> "4 h 50 min"
    return f"{minuti // 60} h {minuti % 60:02d} min"


def main():
    attivita = importa_attivita()
    if not attivita:
        return

    totale = sum(a["durata_minuti"] for a in attivita)
    media = totale / len(attivita)
    # max con key: trova l'attività con la durata più alta
    piu_lunga = max(attivita, key=lambda a: a["durata_minuti"])

    # Somma dei minuti per categoria e per giorno con due dizionari.
    # .get(chiave, 0) restituisce 0 se la chiave non c'è ancora.
    per_categoria = {}
    per_giorno = {}
    for a in attivita:
        categoria = a["categoria"]
        giorno = a["data_ora"].split(" ")[0]   # "2026-09-29 08:15" -> "2026-09-29"
        per_categoria[categoria] = per_categoria.get(categoria, 0) + a["durata_minuti"]
        per_giorno[giorno] = per_giorno.get(giorno, 0) + a["durata_minuti"]

    print("=== STATISTICHE ATTIVITÀ ===")
    print(f"Attività totali : {len(attivita)}")
    print(f"Tempo totale    : {formatta_durata(totale)} ({totale} min)")
    print(f"Durata media    : {media:.1f} min")
    print(f"Più lunga       : {piu_lunga['descrizione']} ({piu_lunga['durata_minuti']} min)")

    print("\nMinuti per categoria (dalla più impegnativa):")
    for categoria, minuti in sorted(per_categoria.items(), key=lambda x: x[1], reverse=True):
        print(f"  {categoria:<10} {minuti:>4} min")

    print("\nMinuti per giorno:")
    for giorno, minuti in sorted(per_giorno.items()):
        print(f"  {giorno}  {minuti:>4} min")


if __name__ == "__main__":
    main()