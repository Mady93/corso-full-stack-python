# Registrazione delle attività nel log.

from .archivio import aggiungi_righe
from .config import FILE_LOG
from .eventi import adesso, evento_a_riga


def nuova_attivita():
    # Il carattere | è il separatore dei campi: lo tolgo dal testo dell'utente
    categoria = input("Categoria: ").strip().lower().replace("|", "/")
    descrizione = input("Descrizione: ").strip().replace("|", "/")
    if not categoria or not descrizione:
        print("Categoria e descrizione sono obbligatorie.")
        return
    durata = input("Durata in minuti: ").strip()
    while not durata.isdigit():
        durata = input("Inserisci un numero intero di minuti: ").strip()
    evento = {"data_ora": adesso(), "categoria": categoria,
              "descrizione": descrizione, "durata": int(durata)}
    aggiungi_righe(FILE_LOG, [evento_a_riga(evento)])
    print("Attività registrata.")