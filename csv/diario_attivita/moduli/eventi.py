# Formato del log: come una riga di testo diventa un evento (dizionario) e viceversa.
# Riga nel file:  data ora | categoria | descrizione | minuti

from datetime import datetime

from .archivio import leggi_righe
from .config import FILE_LOG


def adesso():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def riga_a_evento(riga):
    """Trasforma 'data | cat | descr | min' in dizionario. None se il formato è sbagliato."""
    campi = [c.strip() for c in riga.split("|")]
    if len(campi) != 4 or not campi[3].isdigit():
        return None
    return {"data_ora": campi[0], "categoria": campi[1],
            "descrizione": campi[2], "durata": int(campi[3])}


def evento_a_riga(e):
    return f"{e['data_ora']} | {e['categoria']} | {e['descrizione']} | {e['durata']}"


def leggi_log():
    eventi = (riga_a_evento(r) for r in leggi_righe(FILE_LOG))
    # scarto le righe non valide
    return [e for e in eventi if e is not None]