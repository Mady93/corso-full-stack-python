"""Operazioni CRUD sulla tabella libri."""

# Funzione che apre la connessione a MySQL (definita in db.py)
from database.db import apri_connessione


def inserisci_libro(titolo: str, autore: str, anno: int) -> int:
    """Inserisce un libro e restituisce l'id assegnato dal database."""
    # Apre la connessione e crea il cursore
    connessione = apri_connessione()
    cursor = connessione.cursor()
    try:
        # Query parametrizzata: i valori sono separati dall'SQL (protegge da SQL injection)
        query = """
        INSERT INTO libri (titolo, autore, anno)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (titolo, autore, anno))
        # Conferma l'inserimento (senza commit la modifica non viene salvata)
        connessione.commit()
        return cursor.lastrowid  # id del libro appena inserito
    except Exception:
        # Annulla le modifiche non confermate e rilancia l'errore al chiamante
        connessione.rollback()
        raise
    finally:
        # Chiude sempre cursore e connessione
        cursor.close()
        connessione.close()


def trova_libro(id_libro: int) -> dict | None:
    """Restituisce il libro con quell'id come dizionario, oppure None se non esiste."""
    connessione = apri_connessione()
    # dictionary=True: la riga diventa un dizionario con i nomi delle colonne
    cursor = connessione.cursor(dictionary=True)
    try:
        query = """
        SELECT id, titolo, autore, anno
        FROM libri
        WHERE id = %s
        """
        # La virgola in (id_libro,) serve per creare una tupla con un solo elemento
        cursor.execute(query, (id_libro,))
        return cursor.fetchone()  # None se non esiste
    finally:
        cursor.close()
        connessione.close()


def elenca_libri() -> list[dict]:
    """Restituisce tutti i libri, dal più recente al più vecchio."""
    connessione = apri_connessione()
    cursor = connessione.cursor(dictionary=True)
    try:
        # ORDER BY anno DESC: ordina per anno decrescente
        query = """
        SELECT id, titolo, autore, anno
        FROM libri
        ORDER BY anno DESC
        """
        cursor.execute(query)
        # fetchall() legge tutte le righe del risultato
        return cursor.fetchall()
    finally:
        cursor.close()
        connessione.close()


def libri_dal_anno(anno_minimo: int) -> list[dict]:
    """Restituisce i libri con anno >= anno_minimo, dal più vecchio al più recente."""
    connessione = apri_connessione()
    cursor = connessione.cursor(dictionary=True)
    try:
        # WHERE anno >= %s: filtra con un parametro; ORDER BY anno ASC: ordine crescente
        query = """
        SELECT id, titolo, autore, anno
        FROM libri
        WHERE anno >= %s
        ORDER BY anno ASC
        """
        cursor.execute(query, (anno_minimo,))
        return cursor.fetchall()
    finally:
        cursor.close()
        connessione.close()


def cerca_per_autore(testo: str) -> list[dict]:
    """Restituisce i libri il cui autore contiene il testo indicato (ricerca parziale)."""
    connessione = apri_connessione()
    cursor = connessione.cursor(dictionary=True)
    try:
        # LIKE %s: cerca un testo che contiene il valore, non un valore uguale
        query = """
        SELECT id, titolo, autore, anno
        FROM libri
        WHERE autore LIKE %s
        ORDER BY titolo ASC
        """
        # I jolly % vanno nel valore, non nella query: %Umberto% = contiene "Umberto"
        cursor.execute(query, (f"%{testo}%",))
        return cursor.fetchall()
    finally:
        cursor.close()
        connessione.close()


def modifica_anno(id_libro: int, nuovo_anno: int) -> int:
    """Modifica l'anno di un libro e restituisce il numero di righe modificate."""
    connessione = apri_connessione()
    cursor = connessione.cursor()
    try:
        # WHERE id = %s: modifica solo il libro indicato
        query = """
        UPDATE libri
        SET anno = %s
        WHERE id = %s
        """
        cursor.execute(query, (nuovo_anno, id_libro))
        connessione.commit()
        # rowcount: quante righe ha toccato l'UPDATE (0 se l'id non esiste)
        return cursor.rowcount
    except Exception:
        connessione.rollback()
        raise
    finally:
        cursor.close()
        connessione.close()


def elimina_libro(id_libro: int) -> int:
    """Elimina il libro con quell'id e restituisce il numero di righe eliminate."""
    connessione = apri_connessione()
    cursor = connessione.cursor()
    try:
        # DELETE con WHERE: senza WHERE cancellerebbe tutta la tabella
        query = "DELETE FROM libri WHERE id = %s"
        cursor.execute(query, (id_libro,))
        connessione.commit()
        # rowcount: 1 se ha eliminato il libro, 0 se l'id non esiste
        return cursor.rowcount
    except Exception:
        connessione.rollback()
        raise
    finally:
        cursor.close()
        connessione.close()