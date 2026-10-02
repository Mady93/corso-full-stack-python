"""Creazione del database registro_scuola e della tabella studenti."""

# Funzione che apre la connessione a MySQL (definita in db.py)
from database.db import apri_connessione


def crea_tabella() -> None:
    """Crea la tabella studenti se non esiste già."""
    connessione = apri_connessione()
    cursor = connessione.cursor()

    try:
        query = """
        CREATE TABLE IF NOT EXISTS studenti (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            cognome VARCHAR(100) NOT NULL,
            classe VARCHAR(10) NOT NULL,
            email VARCHAR(150) NOT NULL UNIQUE
        )
        """
        cursor.execute(query)
        connessione.commit()
    finally:
        cursor.close()
        connessione.close()