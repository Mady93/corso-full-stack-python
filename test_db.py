import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

CONFIG_DB = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}


def apri_connessione():
    return mysql.connector.connect(**CONFIG_DB)


def verifica_connessione():
    """Prova la connessione e stampa l'esito. Restituisce True se va a buon fine, altrimenti False."""
    connessione = None
    cursor = None
    try:
        connessione = apri_connessione()
        print("[CONNESSIONE] Connesso:", connessione.is_connected())
        cursor = connessione.cursor()
        cursor.execute("SELECT VERSION()")
        print("[CONNESSIONE] Versione MySQL:", cursor.fetchone()[0])
        return True
    except Error as errore:
        print(f"[CONNESSIONE] ERRORE: {errore}")
        return False
    finally:
        if cursor is not None:
            cursor.close()
        if connessione is not None and connessione.is_connected():
            connessione.close()