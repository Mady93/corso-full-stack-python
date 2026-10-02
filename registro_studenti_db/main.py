"""Registro studenti: menu testuale per gestire la tabella studenti su MySQL."""

# Serve per fermare il programma con sys.exit
import sys
# Classe base degli errori di MySQL
from mysql.connector import Error, IntegrityError
# Funzione che prova la connessione e stampa l'esito (True/False)
from database.db import verifica_connessione
# Creazione di database e tabella
from registro_studenti_db.schema import crea_tabella
# Operazioni sulla tabella studenti
from registro_studenti_db.studenti import (
    inserisci_studente,
    inserisci_studenti_batch,
    trova_studente,
    elenca_studenti,
    cerca_studenti,
    modifica_classe,
    elimina_studente,
)

from registro_studenti_db.status import (
    OK,
    CREATED,
    NO_CONTENT,
    BAD_REQUEST,
    NOT_FOUND,
    INTERNAL_SERVER_ERROR
)

from registro_studenti_db.importa_csv import leggi_csv

def stampa_esito(status: int, messaggio: str) -> None:
    """Stampa lo status e il relativo messaggio."""
    print(f"[{status}] {messaggio}")

# ---------- Funzioni di supporto per input e stampa ----------

def leggi_testo(messaggio: str) -> str:
    """Chiede un testo da tastiera e lo richiede finché non è vuoto."""
    while True:
        valore = input(messaggio).strip()
        if valore:
            return valore
        print("   Il campo non può essere vuoto.")


def leggi_intero(messaggio: str) -> int:
    """Chiede un numero intero da tastiera e lo richiede finché non è valido."""
    while True:
        try:
            return int(input(messaggio).strip())
        except ValueError:
            print("   Inserisci un numero intero.")


def stampa_studenti(studenti: list[dict]) -> None:
    """Stampa gli studenti uno per riga, oppure un messaggio se la lista è vuota."""
    if not studenti:
        print("   (nessuno studente trovato)")
        return
    for s in studenti:
        print(f"   {s['id']:>3} | {s['cognome']} {s['nome']} | classe {s['classe']} | {s['email']}")


# ---------- Azioni del menu ----------

def azione_inserisci() -> None:
    """Inserisce un nuovo studente."""
    nome = leggi_testo("Nome: ")
    cognome = leggi_testo("Cognome: ")
    classe = leggi_testo("Classe (es. 3A): ")
    email = leggi_testo("Email: ")

    try:
        id_nuovo = inserisci_studente(nome, cognome, classe, email)
    except IntegrityError:
        stampa_esito(
            BAD_REQUEST,
            f"Email '{email}' già usata da un altro studente."
        )
        return

    stampa_esito(
        CREATED,
        f"Studente inserito con successo: id={id_nuovo} -> "
        f"{cognome} {nome} | classe {classe} | {email}"
    )


def azione_elenca() -> None:
    """Stampa tutti gli studenti."""
    studenti = elenca_studenti()

    if not studenti:
        stampa_esito(
            NOT_FOUND,
            "Nessuno studente presente nel database."
        )
        return

    stampa_esito(
        OK,
        f"Trovati {len(studenti)} studenti."
    )

    stampa_studenti(studenti)


def azione_cerca() -> None:
    """Cerca studenti per nome o cognome."""
    testo = leggi_testo(
        "Testo da cercare nel nome o cognome: "
    )

    studenti = cerca_studenti(testo)

    if not studenti:
        stampa_esito(
            NOT_FOUND,
            f"Nessuno studente trovato per '{testo}'."
        )
        return

    stampa_esito(
        OK,
        f"Trovati {len(studenti)} studenti."
    )

    stampa_studenti(studenti)


def azione_modifica() -> None:
    """Modifica la classe di uno studente."""
    id_studente = leggi_intero(
        "Id dello studente da modificare: "
    )

    prima = trova_studente(id_studente)

    if prima is None:
        stampa_esito(
            NOT_FOUND,
            f"Studente con id={id_studente} non trovato."
        )
        return

    nuova_classe = leggi_testo(
        f"Nuova classe (attuale {prima['classe']}): "
    )

    righe = modifica_classe(
        id_studente,
        nuova_classe
    )

    if righe == 1:
        stampa_esito(
            OK,
            f"Classe modificata: "
            f"{prima['cognome']} {prima['nome']} | "
            f"{prima['classe']} -> {nuova_classe}"
        )
    else:
        stampa_esito(
            INTERNAL_SERVER_ERROR,
            "Nessuna riga modificata."
        )


def azione_elimina() -> None:
    """Elimina uno studente dopo conferma."""
    id_studente = leggi_intero(
        "Id dello studente da eliminare: "
    )

    studente = trova_studente(id_studente)

    if studente is None:
        stampa_esito(
            NOT_FOUND,
            f"Studente con id={id_studente} non trovato."
        )
        return

    conferma = input(
        f"Eliminare {studente['cognome']} "
        f"{studente['nome']}? (s/n): "
    ).strip().lower()

    if conferma != "s":
        stampa_esito(
            OK,
            "Operazione annullata."
        )
        return

    righe = elimina_studente(id_studente)

    if righe == 1:
        stampa_esito(
            NO_CONTENT,
            f"Studente eliminato: "
            f"{studente['cognome']} {studente['nome']}"
        )
    else:
        stampa_esito(
            INTERNAL_SERVER_ERROR,
            "Nessuno studente eliminato."
        )


def azione_importa() -> None:
    """Importa studenti da un file CSV."""
    percorso = leggi_testo("Percorso del file CSV: ")

    try:
        valide, scartate = leggi_csv(percorso)
    except FileNotFoundError:
        stampa_esito(NOT_FOUND, f"File '{percorso}' non trovato.")
        return
    except KeyError as errore:
        stampa_esito(
            BAD_REQUEST,
            f"Colonna mancante nel CSV: {errore}. "
            "Servono: nome, cognome, classe, email."
        )
        return

    # La funzione batch ora restituisce tre valori
    inseriti, gia_presenti, conflitti = 0, 0, []
    if valide:
        inseriti, gia_presenti, conflitti = inserisci_studenti_batch(valide)

    riepilogo = (
        f"{inseriti} inseriti, {gia_presenti} già presenti, "
        f"{len(conflitti)} in conflitto, {len(scartate)} scartati"
    )

    if not scartate and not conflitti:
        stampa_esito(CREATED, f"Importazione completata: {riepilogo}.")
        return

    stampa_esito(BAD_REQUEST, f"Importazione parziale: {riepilogo}.")
    for s in scartate:
        print(f"   riga {s['riga']}: {s['motivo']}")
    for c in conflitti:
        print(f"   {c['studente']} ({c['email']}): {c['motivo']}")


# ---------- Menu principale ----------

def stampa_menu() -> None:
    """Stampa le voci del menu."""
    print()
    print("------ REGISTRO STUDENTI ------")
    print("1. Inserisci studente")
    print("2. Elenca studenti")
    print("3. Cerca studente (nome o cognome)")
    print("4. Modifica classe")
    print("5. Elimina studente")
    print("6. Importa studenti da CSV")
    print("0. Esci")


def main() -> None:
    """Verifica la connessione, prepara la tabella e mostra il menu."""

    # Verifica una sola volta la connessione al database indicato nel .env
    if not verifica_connessione():
        sys.exit(1)

    # Crea la tabella se non esiste
    try:
        crea_tabella()
        print("[TABELLA] studenti pronta")
    except Error as errore:
        stampa_esito(
            INTERNAL_SERVER_ERROR,
            f"Errore MySQL durante la creazione della tabella: {errore}"
        )
        sys.exit(1)

    # Associa ogni scelta del menu alla sua funzione
    azioni = {
        "1": azione_inserisci,
        "2": azione_elenca,
        "3": azione_cerca,
        "4": azione_modifica,
        "5": azione_elimina,
        "6": azione_importa,
    }

    while True:
        stampa_menu()
        scelta = input("Scelta: ").strip()

        if scelta == "0":
            print("Arrivederci.")
            break

        azione = azioni.get(scelta)

        if azione is None:
            print("Scelta non valida.")
            continue

        try:
            azione()
        except Error as errore:
            print(f"[ERRORE] MySQL: {errore}")


if __name__ == "__main__":
    main()