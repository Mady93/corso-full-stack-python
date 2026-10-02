"""Analisi ricorsiva di una cartella: conteggi, dimensioni, estensioni, date."""

from __future__ import annotations

import os
from collections import Counter
from pathlib import Path
from typing import Any, Dict

from .utilita import formatta_data, formatta_dimensione

# Le statistiche sono un dizionario con chiavi di testo (file, cartelle, dimensione, ...)
Statistiche = Dict[str, Any]


def analizza_cartella(percorso: Path | str) -> Statistiche:
    """Attraversa la cartella e tutte le sottocartelle raccogliendo statistiche.

    Args:
        percorso: cartella da analizzare.

    Returns:
        Dizionario con: file, cartelle (sottocartelle, radice esclusa), dimensione (byte),
        estensioni (Counter), piu_grande e piu_recente (percorso relativo + valore),
        profondita (0 = solo la radice) ed errori (elementi non leggibili).
    """
    radice = Path(percorso)
    r: Statistiche = {
        "percorso": radice,
        "file": 0,
        "cartelle": 0,
        "dimensione": 0,
        "estensioni": Counter(),  # Counter = dizionario che conta quante volte compare ogni chiave
        "piu_grande": None,
        "piu_recente": None,
        "profondita": 0,
        "errori": 0,
    }

    def errore(_: OSError) -> None:
        """Chiamata da os.walk quando non riesce a leggere una cartella: la conto e vado avanti."""
        r["errori"] += 1

    # os.walk visita ricorsivamente: a ogni giro dà (cartella, nomi sottocartelle, nomi file)
    for cartella, sottocartelle, nomi_file in os.walk(radice, onerror=errore):
        cartella = Path(cartella)
        # relative_to() toglie la radice dal percorso; .parts lo spezza in pezzi: quanti pezzi = livello
        livello = len(cartella.relative_to(radice).parts)
        r["profondita"] = max(r["profondita"], livello)
        r["cartelle"] += len(sottocartelle)

        for nome in nomi_file:
            p = cartella / nome
            try:
                st = p.stat()  # stat() legge i metadati (dimensione, data di modifica)
            except OSError:  # es. collegamento rotto o accesso negato
                r["errori"] += 1
                continue

            r["file"] += 1
            r["dimensione"] += st.st_size
            # suffix = estensione (".txt"); se è vuota uso "(nessuna)"
            r["estensioni"][p.suffix.lower() or "(nessuna)"] += 1

            relativo = p.relative_to(radice)
            if r["piu_grande"] is None or st.st_size > r["piu_grande"][1]:
                r["piu_grande"] = (relativo, st.st_size)
            if r["piu_recente"] is None or st.st_mtime > r["piu_recente"][1]:
                r["piu_recente"] = (relativo, st.st_mtime)  # st_mtime = data ultima modifica
    return r


def stampa_analisi(r: Statistiche) -> None:
    """Stampa il riepilogo prodotto da analizza_cartella()."""
    print("\nANALISI CARTELLA")
    print(f"Percorso                  : {r['percorso']}")
    print(f"file totali               : {r['file']}")
    print(f"cartelle totali           : {r['cartelle']}")
    print(f"spazio occupato           : {formatta_dimensione(r['dimensione'])} "
          f"({r['dimensione']} byte)")

    if r["estensioni"]:
        # most_common() ordina le estensioni dalla più frequente alla meno frequente
        elenco = ", ".join(f"{e} ({n})" for e, n in r["estensioni"].most_common())
        frequente, quante = r["estensioni"].most_common(1)[0]
        print(f"estensioni presenti       : {elenco}")
        print(f"estensione più frequente  : {frequente} ({quante} file)")
    else:
        print("estensioni presenti       : -")
        print("estensione più frequente  : -")

    if r["piu_grande"]:
        nome, byte = r["piu_grande"]
        print(f"file più grande           : {nome} ({formatta_dimensione(byte)})")
        nome, quando = r["piu_recente"]
        print(f"modificato più di recente : {nome} ({formatta_data(quando)})")
    else:
        print("file più grande           : -")
        print("modificato più di recente : -")

    print(f"profondità massima        : {r['profondita']}")
    if r["errori"]:
        print(f"elementi non leggibili    : {r['errori']}")