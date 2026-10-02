"""Creazione del database, delle tabelle e delle categorie predefinite."""

from pathlib import Path

from database.db import apri_connessione
from rubrica_db_lab.config import NOME_DB

# Percorso dello script SQL (nella stessa cartella di questo file)
FILE_SCHEMA: Path = Path(__file__).parent / "schema.sql"
CATEGORIE_PREDEFINITE: list[str] = ["Famiglia", "Amici", "Lavoro", "Scuola", "Altro"]


def crea_database() -> None:
    """Crea il database se non esiste già."""
    # Il nome entra in una f-string perché MySQL non accetta %s per i nomi: lo controlliamo
    if not NOME_DB.replace("_", "").isalnum():
        raise ValueError(f"Nome database non valido: {NOME_DB}")
    # database=None: ci si collega solo al server
    connessione = apri_connessione(None)
    cursor = connessione.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {NOME_DB}")
    finally:
        cursor.close()
        connessione.close()


def _leggi_istruzioni() -> list[str]:
    """Legge schema.sql e restituisce le istruzioni, escluse CREATE DATABASE e USE."""
    testo = FILE_SCHEMA.read_text(encoding="utf-8")
    # Toglie le righe di commento
    righe = [r for r in testo.splitlines() if not r.strip().startswith("--")]
    # Separa le istruzioni sul punto e virgola
    istruzioni = [i.strip() for i in "\n".join(righe).split(";") if i.strip()]
    # Il database è già gestito da crea_database()
    return [i for i in istruzioni if not i.upper().startswith(("CREATE DATABASE", "USE "))]


def crea_tabelle() -> None:
    """Esegue le istruzioni CREATE TABLE di schema.sql."""
    connessione = apri_connessione(NOME_DB)
    cursor = connessione.cursor()
    try:
        for istruzione in _leggi_istruzioni():
            cursor.execute(istruzione)
        connessione.commit()
    finally:
        cursor.close()
        connessione.close()


def inserisci_categorie_predefinite() -> None:
    """Inserisce le categorie predefinite con un unico batch (executemany)."""
    connessione = apri_connessione(NOME_DB)
    cursor = connessione.cursor()
    try:
        # INSERT IGNORE: se la categoria esiste già (nome univoco) la salta senza errore
        query = "INSERT IGNORE INTO categorie (nome) VALUES (%s)"
        cursor.executemany(query, [(nome,) for nome in CATEGORIE_PREDEFINITE])
        connessione.commit()
    except Exception:
        connessione.rollback()
        raise
    finally:
        cursor.close()
        connessione.close()


def inizializza() -> None:
    """Prepara tutto: database, tabelle e categorie predefinite."""
    crea_database()
    crea_tabelle()
    inserisci_categorie_predefinite()