"""Esportazione e importazione della rubrica in formato CSV."""

import csv
from pathlib import Path

from database.db import apri_connessione
from rubrica_db_lab.config import NOME_DB
from rubrica_db_lab.categorie import crea_categorie_mancanti, mappa_categorie
from rubrica_db_lab.contatti import (
    SQL_INSERT_CONTATTO,
    SQL_INSERT_LEGAME,
    elenca_contatti,
    normalizza,
    valida_recapiti,
)

# Colonne del file CSV (le categorie sono separate da "|")
COLONNE: list[str] = ["nome", "cognome", "telefono", "email", "note", "categorie"]
# Lunghezze massime, uguali a quelle delle colonne SQL
LIMITI: dict[str, int] = {"nome": 80, "cognome": 80, "telefono": 30, "email": 150, "note": 255}


def esporta_csv(percorso: Path) -> int:
    """Esporta tutti i contatti in un file CSV e restituisce quanti ne ha scritti."""
    contatti = elenca_contatti()
    # utf-8-sig: Excel legge correttamente le lettere accentate; ";" è il separatore di Excel italiano
    with open(percorso, "w", newline="", encoding="utf-8-sig") as file:
        scrittore = csv.DictWriter(file, fieldnames=COLONNE, delimiter=";")
        scrittore.writeheader()
        for c in contatti:
            # I valori None (NULL) diventano stringhe vuote
            scrittore.writerow({colonna: c[colonna] or "" for colonna in COLONNE})
    return len(contatti)


def _chiave(nome: str, cognome: str, telefono: str | None, email: str | None) -> tuple:
    """Chiave per riconoscere i duplicati: l'email se c'è, altrimenti nome+cognome+telefono."""
    if email:
        return ("email", email.lower())
    return ("persona", nome.lower(), cognome.lower(), telefono or "")


def _valida(dati: dict[str, str | None]) -> str | None:
    """Controlla una riga del CSV e restituisce un messaggio di errore, oppure None."""
    if not dati["nome"] or not dati["cognome"]:
        return "nome e cognome obbligatori"
    errore = valida_recapiti(dati["telefono"], dati["email"])
    if errore:
        return errore
    for campo, massimo in LIMITI.items():
        if dati[campo] and len(dati[campo]) > massimo:
            return f"{campo} troppo lungo (massimo {massimo} caratteri)"
    return None


def importa_csv(percorso: Path) -> dict:
    """Importa contatti da CSV in un'unica transazione e restituisce un riepilogo."""
    riepilogo: dict = {"letti": 0, "importati": 0, "duplicati": 0, "non_validi": 0, "scarti": []}

    with open(percorso, newline="", encoding="utf-8-sig") as file:
        # Riconosce il separatore dalla prima riga (";" o ",")
        intestazione = file.readline()
        file.seek(0)
        delimitatore = ";" if intestazione.count(";") > intestazione.count(",") else ","
        lettore = csv.DictReader(file, delimiter=delimitatore)
        # Nomi delle colonne in minuscolo e senza spazi
        lettore.fieldnames = [f.strip().lower() for f in (lettore.fieldnames or [])]
        mancanti = {"nome", "cognome"} - set(lettore.fieldnames)
        if mancanti:
            raise ValueError(f"Colonne obbligatorie mancanti: {', '.join(sorted(mancanti))}")
        righe = list(lettore)

    # Chiavi dei contatti già presenti, per riconoscere i duplicati
    chiavi: set[tuple] = {
        _chiave(c["nome"], c["cognome"], c["telefono"], c["email"]) for c in elenca_contatti()
    }

    # Validazione di tutte le righe prima di toccare il database
    validi: list[tuple[dict, list[str]]] = []
    for numero, riga in enumerate(righe, start=2):
        riepilogo["letti"] += 1
        dati = {campo: normalizza(riga.get(campo)) for campo in LIMITI}
        errore = _valida(dati)
        if errore:
            riepilogo["non_validi"] += 1
            riepilogo["scarti"].append(f"riga {numero}: {errore}")
            continue
        chiave = _chiave(dati["nome"], dati["cognome"], dati["telefono"], dati["email"])
        if chiave in chiavi:
            riepilogo["duplicati"] += 1
            riepilogo["scarti"].append(f"riga {numero}: contatto già presente")
            continue
        # Aggiunge la chiave anche per riconoscere i duplicati dentro lo stesso file
        chiavi.add(chiave)
        nomi_categorie = [n.strip() for n in (riga.get("categorie") or "").split("|") if n.strip()]
        validi.append((dati, nomi_categorie))

    if not validi:
        return riepilogo

    # Batch: crea con una sola chiamata le categorie nuove, poi legge la mappa nome -> id
    crea_categorie_mancanti({n for _, nomi in validi for n in nomi})
    mappa = mappa_categorie()

    connessione = apri_connessione(NOME_DB)
    cursor = connessione.cursor()
    try:
        legami: list[tuple[int, int]] = []
        for dati, nomi in validi:
            cursor.execute(
                SQL_INSERT_CONTATTO,
                (dati["nome"], dati["cognome"], dati["telefono"], dati["email"], dati["note"]),
            )
            # lastrowid serve per collegare le categorie, quindi i contatti si inseriscono uno a uno
            id_contatto = cursor.lastrowid
            legami.extend((id_contatto, cid) for cid in {mappa[n.lower()] for n in nomi})
        if legami:
            # Batch: tutti i legami in una sola chiamata
            cursor.executemany(SQL_INSERT_LEGAME, legami)
        # Un solo commit: se qualcosa fallisce non viene importato nulla
        connessione.commit()
        riepilogo["importati"] = len(validi)
    except Exception:
        connessione.rollback()
        raise
    finally:
        cursor.close()
        connessione.close()
    return riepilogo