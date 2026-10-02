"""Operazioni sulla tabella categorie."""

from database.db import apri_connessione
from rubrica_db_lab.config import NOME_DB


def elenca_categorie() -> list[dict]:
    """Restituisce tutte le categorie in ordine alfabetico."""
    connessione = apri_connessione(NOME_DB)
    cursor = connessione.cursor(dictionary=True)
    try:
        query = "SELECT id, nome FROM categorie ORDER BY nome ASC"
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        connessione.close()


def mappa_categorie() -> dict[str, int]:
    """Restituisce un dizionario nome (minuscolo) -> id."""
    return {c["nome"].lower(): c["id"] for c in elenca_categorie()}


def crea_categoria(nome: str) -> int:
    """Crea la categoria se non esiste e restituisce il suo id."""
    connessione = apri_connessione(NOME_DB)
    cursor = connessione.cursor()
    try:
        cursor.execute("INSERT IGNORE INTO categorie (nome) VALUES (%s)", (nome,))
        connessione.commit()
        # Rilegge l'id (anche se la categoria esisteva già)
        cursor.execute("SELECT id FROM categorie WHERE nome = %s", (nome,))
        return cursor.fetchone()[0]
    except Exception:
        connessione.rollback()
        raise
    finally:
        cursor.close()
        connessione.close()


def crea_categorie_mancanti(nomi: set[str]) -> None:
    """Crea con un unico batch le categorie che non esistono ancora."""
    if not nomi:
        return
    connessione = apri_connessione(NOME_DB)
    cursor = connessione.cursor()
    try:
        query = "INSERT IGNORE INTO categorie (nome) VALUES (%s)"
        cursor.executemany(query, [(nome,) for nome in sorted(nomi)])
        connessione.commit()
    except Exception:
        connessione.rollback()
        raise
    finally:
        cursor.close()
        connessione.close()