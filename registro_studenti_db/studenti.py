"""Operazioni CRUD sulla tabella studenti."""

# Funzione che apre la connessione a MySQL (definita in db.py)
from database.db import apri_connessione

def inserisci_studente(nome: str, cognome: str, classe: str, email: str) -> int:
    """Inserisce uno studente e restituisce l'id assegnato dal database."""
    connessione = apri_connessione()
    cursor = connessione.cursor()
    try:
        # Query parametrizzata: i valori sono separati dall'SQL
        query = """
        INSERT INTO studenti (nome, cognome, classe, email)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (nome, cognome, classe, email))
        # Conferma l'inserimento
        connessione.commit()
        return cursor.lastrowid  # id dello studente appena inserito
    except Exception:
        # Annulla le modifiche non confermate e rilancia l'errore
        connessione.rollback()
        raise
    finally:
        cursor.close()
        connessione.close()


def inserisci_studenti_batch(studenti: list[tuple]) -> tuple[int, int, list[dict]]:
    """Inserisce molti studenti in un'unica transazione.
    Restituisce (inseriti, gia_presenti, conflitti)."""
    connessione = apri_connessione()
    cursor = connessione.cursor(dictionary=True)
    inseriti = 0
    gia_presenti = 0
    conflitti = []
    try:
        for nome, cognome, classe, email in studenti:
            cursor.execute(
                "SELECT id, nome, cognome FROM studenti WHERE email = %s",
                (email,)
            )
            esistente = cursor.fetchone()

            if esistente is None:
                cursor.execute(
                    """
                    INSERT INTO studenti (nome, cognome, classe, email)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (nome, cognome, classe, email)
                )
                inseriti += 1
            elif (esistente["nome"].lower(), esistente["cognome"].lower()) == (nome.lower(), cognome.lower()):
                gia_presenti += 1
            else:
                conflitti.append({
                    "email": email,
                    "studente": f"{cognome} {nome}",
                    "motivo": f"email già usata da {esistente['cognome']} {esistente['nome']} (id {esistente['id']})",
                })

        connessione.commit()
        return inseriti, gia_presenti, conflitti
    except Exception:
        connessione.rollback()
        raise
    finally:
        cursor.close()
        connessione.close()
        

def trova_studente(id_studente: int) -> dict | None:
    """Restituisce lo studente con quell'id, oppure None se non esiste."""
    connessione = apri_connessione()
    # dictionary=True: ogni riga diventa un dizionario con i nomi delle colonne
    cursor = connessione.cursor(dictionary=True)
    try:
        query = """
        SELECT id, nome, cognome, classe, email
        FROM studenti
        WHERE id = %s
        """
        cursor.execute(query, (id_studente,))
        return cursor.fetchone()  # None se non esiste
    finally:
        cursor.close()
        connessione.close()


def elenca_studenti() -> list[dict]:
    """Restituisce tutti gli studenti in ordine alfabetico di cognome e nome."""
    connessione = apri_connessione()
    cursor = connessione.cursor(dictionary=True)
    try:
        query = """
        SELECT id, nome, cognome, classe, email
        FROM studenti
        ORDER BY cognome ASC, nome ASC
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        connessione.close()


def cerca_studenti(testo: str) -> list[dict]:
    """Restituisce gli studenti il cui nome o cognome contiene il testo indicato."""
    connessione = apri_connessione()
    cursor = connessione.cursor(dictionary=True)
    try:
        # LIKE con due parametri: uno per il nome e uno per il cognome
        query = """
        SELECT id, nome, cognome, classe, email
        FROM studenti
        WHERE nome LIKE %s OR cognome LIKE %s
        ORDER BY cognome ASC, nome ASC
        """
        # I jolly % vanno nel valore, non nella query
        modello = f"%{testo}%"
        cursor.execute(query, (modello, modello))
        return cursor.fetchall()
    finally:
        cursor.close()
        connessione.close()


def modifica_classe(id_studente: int, nuova_classe: str) -> int:
    """Modifica la classe di uno studente e restituisce il numero di righe modificate."""
    connessione = apri_connessione()
    cursor = connessione.cursor()
    try:
        query = """
        UPDATE studenti
        SET classe = %s
        WHERE id = %s
        """
        cursor.execute(query, (nuova_classe, id_studente))
        connessione.commit()
        # rowcount: quante righe ha toccato l'UPDATE (0 se l'id non esiste)
        return cursor.rowcount
    except Exception:
        connessione.rollback()
        raise
    finally:
        cursor.close()
        connessione.close()


def elimina_studente(id_studente: int) -> int:
    """Elimina lo studente con quell'id e restituisce il numero di righe eliminate."""
    connessione = apri_connessione()
    cursor = connessione.cursor()
    try:
        # Senza WHERE cancellerebbe tutta la tabella
        query = "DELETE FROM studenti WHERE id = %s"
        cursor.execute(query, (id_studente,))
        connessione.commit()
        # rowcount: 1 se ha eliminato lo studente, 0 se l'id non esiste
        return cursor.rowcount
    except Exception:
        connessione.rollback()
        raise
    finally:
        cursor.close()
        connessione.close()