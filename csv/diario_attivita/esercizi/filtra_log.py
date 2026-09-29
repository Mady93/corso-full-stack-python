# Esercizio 5 - Filtro log
#
# Realizza un programma che analizzi un log esistente e 
# visualizzi solo gli eventi che rispettano un criterio scelto dall'utente.
#
# Concetti: split() per dividere una riga in campi, list comprehension, startswith().

import os

# Questo file sta in esercizi/: la cartella del progetto è quella sopra
CARTELLA_PROGETTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARTELLA_DATI = os.path.join(CARTELLA_PROGETTO, "dati")
FILE_LOG = os.path.join(CARTELLA_DATI, "attivita.log")


def leggi_log():
    """Legge il log e restituisce una lista di dizionari (uno per evento)."""
    if not os.path.exists(FILE_LOG):
        return []

    eventi = []
    with open(FILE_LOG, "r", encoding="utf-8") as file:
        for riga in file:
            # "a | b | c | d" -> ["a", "b", "c", "d"] (strip toglie gli spazi)
            campi = [c.strip() for c in riga.strip().split("|")]
            # Salto le righe con formato sbagliato
            if len(campi) == 4 and campi[3].isdigit():
                eventi.append({
                    "data_ora": campi[0],
                    "categoria": campi[1],
                    "descrizione": campi[2],
                    "durata": int(campi[3]),
                })
    return eventi


def stampa_eventi(eventi):
    if not eventi:
        print("Nessun evento corrisponde al criterio.")
        return
    print(f"\n{'DATA E ORA':<16} {'CATEGORIA':<10} {'DESCRIZIONE':<36} {'MIN':>4}")
    print("-" * 70)
    for e in eventi:
        print(f"{e['data_ora']:<16} {e['categoria']:<10} "
              f"{e['descrizione']:<36} {e['durata']:>4}")
    print(f"\n{len(eventi)} eventi")


def main():
    eventi = leggi_log()
    if not eventi:
        print("Log mancante o vuoto: esegui prima registra_attivita.py")
        return

    print("Filtra per:")
    print("1) Categoria")
    print("2) Data (AAAA-MM-GG)")
    print("3) Durata minima (minuti)")
    print("4) Parola nella descrizione")
    scelta = input("Scelta: ").strip()

    if scelta == "1":
        valore = input("Categoria: ").strip().lower()
        risultati = [e for e in eventi if e["categoria"].lower() == valore]
    elif scelta == "2":
        valore = input("Data: ").strip()
        # startswith: "2026-09-29" corrisponde a "2026-09-29 08:15"
        risultati = [e for e in eventi if e["data_ora"].startswith(valore)]
    elif scelta == "3":
        valore = input("Durata minima: ").strip()
        if not valore.isdigit():
            print("Numero non valido.")
            return
        risultati = [e for e in eventi if e["durata"] >= int(valore)]
    elif scelta == "4":
        valore = input("Parola: ").strip().lower()
        risultati = [e for e in eventi if valore in e["descrizione"].lower()]
    else:
        print("Scelta non valida.")
        return

    stampa_eventi(risultati)


if __name__ == "__main__":
    main()