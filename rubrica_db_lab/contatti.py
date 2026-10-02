"""Operazioni CRUD e ricerca sulla tabella contatti."""

from database.db import apri_connessione
from rubrica_db_lab.config import NOME_DB

# Colonne modificabili: elenco fisso (whitelist) usato per costruire gli UPDATE in sicurezza
CAMPI_MODIFICABILI: tuple[str, ...] = ("nome", "cognome", "telefono", "email", "note")

# Criteri di ricerca testuali: criterio -> colonna SQL (elenco fisso, mai input dell'utente)
CAMPI_RICERCA: dict[str, str] = {
    "nome": "c.nome",
    "cognome": "c.cognome",
    "telefono": "c.telefono",
    "email": "c.email",
}

# Query riutilizzate anche dall'importazione CSV
SQL_INSERT_CONTATTO = """
INSERT INTO contatti (nome, cognome, telefono, email, note)
VALUES (%s, %s, %s, %s, %s)
"""
SQL_INSERT_LEGAME = """
INSERT INTO contatti_categorie (contatto_id, categoria_id)
VALUES (%s, %s)
"""
# Le categorie di ogni contatto sono unite in una stringa separata da "|"
SQL_SELECT_CONTATTI = """
SELECT c.id, c.nome, c.cognome, c.telefono, c.email, c.note,
       GROUP_CONCAT(k.nome ORDER BY k.nome SEPARATOR '|') AS categorie
FROM contatti c
LEFT JOIN contatti_categorie cc ON cc.contatto_id = c.id
LEFT JOIN categorie k ON k.id = cc.categoria_id
"""
SQL_ORDINE = """
GROUP BY c.id
ORDER BY c.cognome ASC, c.nome ASC
"""


def normalizza(valore: str | None) -> str | None:
    """Toglie gli spazi e trasforma le stringhe vuote in None (NULL nel database)."""
    if valore is None:
        return None
    valore = valore.strip()
    return valore or None


def valida_recapiti(telefono: str | None, email: str | None) -> str | None:
    """Restituisce un messaggio di errore se i recapiti non sono validi, altrimenti None."""
    if not telefono and not email:
        return "serve almeno un telefono o un'email"
    if email and "@" not in email:
        return "email non valida"
    return None


def _leggi(query: str, parametri: tuple = ()) -> list[dict]:
    """Esegue una SELECT e restituisce le righe come dizionari."""
    connessione = apri_connessione(NOME_DB)
    cursor = connessione.cursor(dictionary=True)
    try:
        cursor.execute(query, parametri)
        return cursor.fetchall()
    finally:
        cursor.close()
        connessione.close()


def inserisci_contatto(
    nome: str,
    cognome: str,
    telefono: str | None,
    email: str | None,
    note: str | None,
    categorie_ids: list[int],
) -> int:
    """Inserisce un contatto con le sue categorie in un'unica transazione."""
    connessione = apri_connessione(NOME_DB)
    cursor = connessione.cursor()
    try:
        cursor.execute(
            SQL_INSERT_CONTATTO,
            (nome, cognome, normalizza(telefono), normalizza(email), normalizza(note)),
        )
        id_contatto = cursor.lastrowid
        if categorie_ids:
            # Batch: tutti i legami contatto-categoria in una sola chiamata
            legami = [(id_contatto, cid) for cid in sorted(set(categorie_ids))]
            cursor.executemany(SQL_INSERT_LEGAME, legami)
        # Un solo commit: o si salva tutto o niente
        connessione.commit()
        return id_contatto
    except Exception:
        connessione.rollback()
        raise
    finally:
        cursor.close()
        connessione.close()


def elenca_contatti() -> list[dict]:
    """Restituisce tutti i contatti in ordine di cognome e nome."""
    return _leggi(SQL_SELECT_CONTATTI + SQL_ORDINE)


def trova_contatto(id_contatto: int) -> dict | None:
    """Restituisce il contatto con quell'id, oppure None se non esiste."""
    righe = _leggi(SQL_SELECT_CONTATTI + "WHERE c.id = %s\n" + SQL_ORDINE, (id_contatto,))
    return righe[0] if righe else None


def cerca_contatti(criteri: dict[str, str]) -> list[dict]:
    """Cerca i contatti che rispettano TUTTI i criteri indicati (ricerca parziale con LIKE)."""
    condizioni: list[str] = []
    parametri: list[str] = []
    for campo, valore in criteri.items():
        valore = (valore or "").strip()
        # I criteri vuoti vengono ignorati
        if not valore:
            continue
        if campo == "categoria":
            # EXISTS: il contatto deve avere almeno una categoria che contiene il testo
            condizioni.append(
                "EXISTS (SELECT 1 FROM contatti_categorie x "
                "JOIN categorie y ON y.id = x.categoria_id "
                "WHERE x.contatto_id = c.id AND y.nome LIKE %s)"
            )
        elif campo in CAMPI_RICERCA:
            # La colonna viene dall'elenco fisso, il valore resta un parametro
            condizioni.append(f"{CAMPI_RICERCA[campo]} LIKE %s")
        else:
            raise ValueError(f"Criterio di ricerca non valido: {campo}")
        # I jolly % vanno nel valore, non nella query
        parametri.append(f"%{valore}%")
    where = ("WHERE " + " AND ".join(condizioni) + "\n") if condizioni else ""
    return _leggi(SQL_SELECT_CONTATTI + where + SQL_ORDINE, tuple(parametri))


def modifica_contatto(id_contatto: int, campi: dict[str, str | None]) -> int:
    """Modifica uno o più campi di un contatto e restituisce rowcount."""
    if not campi:
        return 0
    assegnazioni: list[str] = []
    parametri: list = []
    for campo, valore in campi.items():
        # Accetta solo le colonne dell'elenco fisso
        if campo not in CAMPI_MODIFICABILI:
            raise ValueError(f"Campo non modificabile: {campo}")
        assegnazioni.append(f"{campo} = %s")
        parametri.append(normalizza(valore))
    parametri.append(id_contatto)
    query = f"UPDATE contatti SET {', '.join(assegnazioni)} WHERE id = %s"
    connessione = apri_connessione(NOME_DB)
    cursor = connessione.cursor()
    try:
        cursor.execute(query, tuple(parametri))
        connessione.commit()
        return cursor.rowcount
    except Exception:
        connessione.rollback()
        raise
    finally:
        cursor.close()
        connessione.close()


def imposta_categorie(id_contatto: int, categorie_ids: list[int]) -> None:
    """Sostituisce le categorie di un contatto (cancella le vecchie e inserisce le nuove)."""
    connessione = apri_connessione(NOME_DB)
    cursor = connessione.cursor()
    try:
        cursor.execute("DELETE FROM contatti_categorie WHERE contatto_id = %s", (id_contatto,))
        if categorie_ids:
            legami = [(id_contatto, cid) for cid in sorted(set(categorie_ids))]
            cursor.executemany(SQL_INSERT_LEGAME, legami)
        connessione.commit()
    except Exception:
        connessione.rollback()
        raise
    finally:
        cursor.close()
        connessione.close()


def elimina_contatto(id_contatto: int) -> int:
    """Elimina un contatto (i legami con le categorie spariscono per ON DELETE CASCADE)."""
    connessione = apri_connessione(NOME_DB)
    cursor = connessione.cursor()
    try:
        cursor.execute("DELETE FROM contatti WHERE id = %s", (id_contatto,))
        connessione.commit()
        return cursor.rowcount
    except Exception:
        connessione.rollback()
        raise
    finally:
        cursor.close()
        connessione.close()