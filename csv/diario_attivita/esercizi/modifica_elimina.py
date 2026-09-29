# Esercizio 9 - Gestione modifiche
#
# Realizza un programma che permetta di modificare 
# o eliminare dati persistenti senza perdere le informazioni non coinvolte.
#
# Metodo: leggo tutte le righe - cambio solo quella scelta nella lista in memoria
# - riscrivo il file con "w". Le righe non coinvolte restano identiche.

import os

# Questo file sta in esercizi/: la cartella del progetto è quella sopra
CARTELLA_PROGETTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARTELLA_DATI = os.path.join(CARTELLA_PROGETTO, "dati")
FILE_LOG = os.path.join(CARTELLA_DATI, "attivita.log")


def leggi_righe():
    """Restituisce le righe del log come lista di stringhe (senza righe vuote)."""
    if not os.path.exists(FILE_LOG):
        return []
    with open(FILE_LOG, "r", encoding="utf-8") as file:
        return [riga.strip() for riga in file if riga.strip()]


def salva_righe(righe):
    # "w" cancella il file e lo riscrive tutto: per questo scrivo TUTTE le righe,
    # comprese quelle che non ho toccato.
    with open(FILE_LOG, "w", encoding="utf-8") as file:
        for riga in righe:
            file.write(riga + "\n")


def mostra(righe):
    if not righe:
        print("Il log è vuoto.")
        return
    for numero, riga in enumerate(righe, start=1):
        print(f"{numero:>3}. {riga}")


def chiedi_indice(righe):
    """Chiede un numero di riga (da 1) e lo converte in indice (da 0). None se non valido."""
    scelta = input("Numero della riga: ").strip()
    if not scelta.isdigit() or not 1 <= int(scelta) <= len(righe):
        print("Numero non valido.")
        return None
    return int(scelta) - 1


def modifica(righe):
    indice = chiedi_indice(righe)
    if indice is None:
        return

    campi = [c.strip() for c in righe[indice].split("|")]
    if len(campi) != 4:
        print("Questa riga non ha il formato standard: non la modifico.")
        return

    print("Premi Invio per mantenere il valore attuale.")
    # "x or y": se l'utente preme solo Invio (stringa vuota) prende il valore vecchio
    categoria = input(f"Categoria [{campi[1]}]: ").strip().lower().replace("|", "/") or campi[1]
    descrizione = input(f"Descrizione [{campi[2]}]: ").strip().replace("|", "/") or campi[2]
    durata = input(f"Durata [{campi[3]}]: ").strip()
    if durata and not durata.isdigit():
        print("Durata non valida: modifica annullata.")
        return

    campi[1] = categoria
    campi[2] = descrizione
    campi[3] = durata or campi[3]
    righe[indice] = " | ".join(campi)   # cambia SOLO questa riga
    salva_righe(righe)
    print("Riga modificata.")


def elimina(righe):
    indice = chiedi_indice(righe)
    if indice is None:
        return
    print("Riga scelta:", righe[indice])
    if input("Confermi l'eliminazione? (s/n): ").strip().lower() != "s":
        print("Eliminazione annullata.")
        return
    del righe[indice]                   # tolgo solo questa riga dalla lista
    salva_righe(righe)
    print("Riga eliminata.")


def main():
    while True:
        righe = leggi_righe()   # rileggo a ogni giro: la lista è sempre aggiornata
        print("\n=== MODIFICA LOG ===")
        print("1) Mostra il log")
        print("2) Modifica una riga")
        print("3) Elimina una riga")
        print("0) Esci")
        scelta = input("Scelta: ").strip()

        if scelta == "1":
            mostra(righe)
        elif scelta == "2":
            mostra(righe)
            if righe:
                modifica(righe)
        elif scelta == "3":
            mostra(righe)
            if righe:
                elimina(righe)
        elif scelta == "0":
            print("Arrivederci!")
            break
        else:
            print("Scelta non valida.")


if __name__ == "__main__":
    main()