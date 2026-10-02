"""Creazione della struttura del database: tabella libri."""

# Funzione che apre la connessione a MySQL (definita in db.py)
from database.db import apri_connessione


def crea_tabella() -> None:
    """Crea la tabella libri se non esiste già."""
    # Apre la connessione al database indicato nel .env
    connessione = apri_connessione()
    # Crea il cursore per eseguire l'SQL
    cursor = connessione.cursor()
    # try/finally: le risorse si chiudono sempre, anche se c'è un errore
    try:
        # IF NOT EXISTS evita l'errore se la tabella esiste già
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS libri (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titolo VARCHAR(150) NOT NULL,
            autore VARCHAR(100) NOT NULL,
            anno INT NOT NULL
        )
        """)
        # Conferma la modifica strutturale
        connessione.commit()
    finally:
        # Chiude prima il cursore e poi la connessione
        cursor.close()
        connessione.close()