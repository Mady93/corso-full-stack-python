"""Configurazione e apertura della connessione a MySQL."""

# Serve per leggere le variabili d'ambiente
import os
# Libreria per collegarsi a MySQL
import mysql.connector
# Classe base degli errori di MySQL
from mysql.connector import Error
# Legge il file .env e carica le variabili
from dotenv import load_dotenv

# Carica host, utente, password e nome database dal file .env
load_dotenv()

# Dizionario con i dati di connessione (il secondo valore è quello di riserva)
CONFIG_DB = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

# Messaggi chiari per gli errori più comuni (chiave = codice errore MySQL)
CAUSE_ERRORI = {
    1045: "credenziali non valide (utente o password errati)",
    1049: "database inesistente (controlla DB_NAME nel file .env)",
    2003: "server MySQL non raggiungibile (spento, host o porta errati)",
}


def apri_connessione():
    """Apre e restituisce una connessione MySQL con i dati di CONFIG_DB."""
    # ** passa le coppie chiave-valore del dizionario come argomenti a connect()
    return mysql.connector.connect(**CONFIG_DB)


def verifica_connessione() -> bool:
    """Prova la connessione e stampa l'esito. Restituisce True se riesce, altrimenti False."""
    # Inizializza a None: se la connessione fallisce, il finally non va in errore
    connessione = None
    cursor = None
    try:
        # Apre la connessione al database
        connessione = apri_connessione()
        # Crea il cursore per eseguire l'SQL
        cursor = connessione.cursor()
        # Chiede al server la versione di MySQL
        cursor.execute("SELECT VERSION()")
        versione = cursor.fetchone()[0]
        # Una sola riga di esito, senza dati sensibili (la password non viene mai stampata)
        print(
            f"[OK] Connessione stabilita: database '{CONFIG_DB['database']}' "
            f"su {CONFIG_DB['host']}:{CONFIG_DB['port']} (MySQL {versione})"
        )
        return True
    except Error as errore:
        # Cerca una spiegazione per il codice errore, altrimenti usa un messaggio generico
        causa = CAUSE_ERRORI.get(errore.errno, "errore durante la connessione")
        print(f"[ERRORE] Connessione non riuscita: {causa}")
        # Il messaggio originale di MySQL resta disponibile per la diagnosi
        print(f"         Dettaglio: {errore}")
        return False
    finally:
        # Chiude il cursore solo se è stato creato
        if cursor is not None:
            cursor.close()
        # Chiude la connessione solo se esiste ed è ancora attiva
        if connessione is not None and connessione.is_connected():
            connessione.close()