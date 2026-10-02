"""Rubrica contatti: applicazione da terminale con persistenza su MySQL."""

import sys
from pathlib import Path

from mysql.connector import Error
from mysql.connector.errors import IntegrityError

from database.db import verifica_connessione
from rubrica_db_lab.config import NOME_DB
from rubrica_db_lab.schema import inizializza
from rubrica_db_lab.categorie import crea_categoria, elenca_categorie
from rubrica_db_lab.contatti import (
    CAMPI_MODIFICABILI,
    cerca_contatti,
    elenca_contatti,
    elimina_contatto,
    imposta_categorie,
    inserisci_contatto,
    modifica_contatto,
    normalizza,
    trova_contatto,
    valida_recapiti,
)
from rubrica_db_lab.csv_io import esporta_csv, importa_csv


# ---------- Input e stampa ----------

def leggi_testo(messaggio: str, obbligatorio: bool = True) -> str:
    """Chiede un testo; se obbligatorio lo richiede finché non è vuoto."""
    while True:
        valore = input(messaggio).strip()
        if valore or not obbligatorio:
            return valore
        print("   Campo obbligatorio.")


def leggi_intero(messaggio: str) -> int:
    """Chiede un numero intero finché non è valido."""
    while True:
        try:
            return int(input(messaggio).strip())
        except ValueError:
            print("   Inserisci un numero intero.")


def conferma(messaggio: str) -> bool:
    """Chiede una conferma s/n."""
    return input(f"{messaggio} (s/n): ").strip().lower() == "s"


def formatta_categorie(contatto: dict) -> str:
    """Rende leggibile la stringa delle categorie."""
    return contatto["categorie"].replace("|", ", ") if contatto["categorie"] else "-"


def stampa_contatti(elenco: list[dict]) -> None:
    """Stampa i contatti, uno per riga."""
    if not elenco:
        print("   (nessun contatto trovato)")
        return
    for c in elenco:
        print(
            f"   {c['id']:>3} | {c['cognome']} {c['nome']} | "
            f"{c['telefono'] or '-'} | {c['email'] or '-'} | {formatta_categorie(c)}"
        )


def stampa_dettaglio(c: dict) -> None:
    """Stampa tutti i dati di un contatto."""
    print(f"   Id:         {c['id']}")
    print(f"   Nome:       {c['nome']}")
    print(f"   Cognome:    {c['cognome']}")
    print(f"   Telefono:   {c['telefono'] or '-'}")
    print(f"   Email:      {c['email'] or '-'}")
    print(f"   Note:       {c['note'] or '-'}")
    print(f"   Categorie:  {formatta_categorie(c)}")


def leggi_categorie() -> list[int]:
    """Mostra le categorie e chiede quali associare (id separati da virgola)."""
    elenco = elenca_categorie()
    print("Categorie disponibili:")
    for c in elenco:
        print(f"   {c['id']:>3} | {c['nome']}")
    testo = input("Id delle categorie separati da virgola (invio = nessuna): ")
    validi = {c["id"] for c in elenco}
    scelti: list[int] = []
    for parte in testo.split(","):
        parte = parte.strip()
        if not parte:
            continue
        if parte.isdigit() and int(parte) in validi:
            scelti.append(int(parte))
        else:
            print(f"   Id '{parte}' ignorato")
    return scelti


# ---------- Azioni del menu ----------

def azione_inserisci() -> None:
    """Inserisce un nuovo contatto."""
    nome = leggi_testo("Nome: ")
    cognome = leggi_testo("Cognome: ")
    telefono = normalizza(input("Telefono: "))
    email = normalizza(input("Email: "))
    note = normalizza(input("Note: "))
    errore = valida_recapiti(telefono, email)
    if errore:
        print(f"[INSERT] annullato: {errore}")
        return
    categorie_ids = leggi_categorie()
    id_nuovo = inserisci_contatto(nome, cognome, telefono, email, note, categorie_ids)
    print(f"[INSERT] id={id_nuovo} -> {cognome} {nome}")
    # Rilegge il contatto per confermare che sia nel database
    esito = "OK" if trova_contatto(id_nuovo) is not None else "KO"
    print(f"   [VERIFICA {esito}] il contatto è presente nel database")


def azione_elenca() -> None:
    """Elenca tutti i contatti."""
    print("[SELECT] rubrica:")
    stampa_contatti(elenca_contatti())


def azione_dettaglio() -> None:
    """Mostra il dettaglio di un contatto."""
    id_contatto = leggi_intero("Id del contatto: ")
    contatto = trova_contatto(id_contatto)
    if contatto is None:
        print(f"[SELECT] id={id_contatto} non trovato")
        return
    stampa_dettaglio(contatto)


def azione_cerca() -> None:
    """Cerca contatti combinando più criteri (tutti devono essere rispettati)."""
    print("Lascia vuoto (invio) i criteri che non vuoi usare.")
    criteri = {
        "nome": input("Nome contiene: "),
        "cognome": input("Cognome contiene: "),
        "telefono": input("Telefono contiene: "),
        "email": input("Email contiene: "),
        "categoria": input("Categoria contiene: "),
    }
    risultati = cerca_contatti(criteri)
    print(f"[SELECT] {len(risultati)} contatti trovati:")
    stampa_contatti(risultati)


def azione_modifica() -> None:
    """Modifica uno o più campi di un contatto."""
    id_contatto = leggi_intero("Id del contatto da modificare: ")
    attuale = trova_contatto(id_contatto)
    if attuale is None:
        print(f"[UPDATE] id={id_contatto} non trovato")
        return
    print("Invio = lascia invariato, '-' = svuota (solo telefono, email, note)")
    campi: dict[str, str | None] = {}
    for campo in CAMPI_MODIFICABILI:
        valore = input(f"{campo.capitalize()} [{attuale[campo] or ''}]: ").strip()
        if not valore:
            continue
        if valore == "-":
            if campo in ("nome", "cognome"):
                print("   Nome e cognome non si possono svuotare.")
                continue
            campi[campo] = None
        else:
            campi[campo] = valore
    # Controlla i vincoli sui valori che il contatto avrà dopo la modifica
    finale = {**attuale, **campi}
    errore = valida_recapiti(finale["telefono"], finale["email"])
    if errore:
        print(f"[UPDATE] annullato: {errore}")
        return
    if campi:
        righe = modifica_contatto(id_contatto, campi)
        print(f"[UPDATE] id={id_contatto} modificato (rowcount={righe})")
        # Rilegge il contatto e confronta ogni campo modificato
        dopo = trova_contatto(id_contatto)
        for campo, valore in campi.items():
            esito = "OK" if dopo is not None and dopo[campo] == normalizza(valore) else "KO"
            print(f"   [VERIFICA {esito}] {campo}: {attuale[campo] or '-'} -> {dopo[campo] or '-'}")
    if conferma("Vuoi modificare anche le categorie?"):
        imposta_categorie(id_contatto, leggi_categorie())
        print(f"[UPDATE] categorie aggiornate: {formatta_categorie(trova_contatto(id_contatto))}")


def azione_elimina() -> None:
    """Elimina un contatto dopo conferma."""
    id_contatto = leggi_intero("Id del contatto da eliminare: ")
    contatto = trova_contatto(id_contatto)
    if contatto is None:
        print(f"[DELETE] id={id_contatto} non trovato, niente da eliminare")
        return
    stampa_dettaglio(contatto)
    if not conferma("Eliminare definitivamente questo contatto?"):
        print("[DELETE] operazione annullata")
        return
    righe = elimina_contatto(id_contatto)
    print(f"[DELETE] id={id_contatto} eliminato (rowcount={righe})")
    esito = "OK" if righe == 1 and trova_contatto(id_contatto) is None else "KO"
    print(f"   [VERIFICA {esito}] il contatto non esiste più")


def azione_categorie() -> None:
    """Sottomenu per elencare, creare e assegnare le categorie."""
    print("1. Elenca categorie")
    print("2. Nuova categoria")
    print("3. Assegna categorie a un contatto")
    scelta = input("Scelta: ").strip()
    if scelta == "1":
        for c in elenca_categorie():
            print(f"   {c['id']:>3} | {c['nome']}")
    elif scelta == "2":
        nome = leggi_testo("Nome della categoria: ")
        if any(carattere in nome for carattere in "|;,"):
            print("   Il nome non può contenere | ; ,")
            return
        print(f"[INSERT] categoria '{nome}' con id={crea_categoria(nome)}")
    elif scelta == "3":
        id_contatto = leggi_intero("Id del contatto: ")
        if trova_contatto(id_contatto) is None:
            print(f"[UPDATE] id={id_contatto} non trovato")
            return
        imposta_categorie(id_contatto, leggi_categorie())
        print(f"[UPDATE] categorie: {formatta_categorie(trova_contatto(id_contatto))}")
    else:
        print("Scelta non valida.")


def azione_esporta() -> None:
    """Esporta la rubrica in un file CSV."""
    nome_file = input(
        "Nome del file CSV da creare [rubrica_export.csv]: "
    ).strip() or "rubrica_export.csv"

    percorso = Path(__file__).parent / nome_file

    totale = esporta_csv(percorso)
    print(f"[EXPORT] {totale} contatti scritti in {percorso.resolve()}")


def azione_importa() -> None:
    """Importa contatti da un file CSV e stampa il riepilogo."""
    nome_file = leggi_testo("File CSV da importare: ")
    percorso = Path(__file__).parent / nome_file

    if not percorso.is_file():
        print(f"[IMPORT] file non trovato: {percorso}")
        return
    try:
        riepilogo = importa_csv(percorso)
    except ValueError as errore:
        print(f"[IMPORT] file non valido: {errore}")
        return
    print("[IMPORT] riepilogo:")
    print(f"righe lette: {riepilogo['letti']}")
    print(f"contatti importati: {riepilogo['importati']}")
    print(f"duplicati saltati: {riepilogo['duplicati']}")
    print(f"righe non valide: {riepilogo['non_validi']}")

    for scarto in riepilogo["scarti"]:
     print(f"- {scarto}")


# ---------- Menu principale ----------

def stampa_menu() -> None:
    """Stampa le voci del menu."""
    print()
    print("----- RUBRICA CONTATTI -----")
    print("1. Nuovo contatto")
    print("2. Elenco contatti")
    print("3. Dettaglio contatto")
    print("4. Cerca contatti")
    print("5. Modifica contatto")
    print("6. Elimina contatto")
    print("7. Categorie")
    print("8. Esporta CSV")
    print("9. Importa CSV")
    print("0. Esci")


def main() -> None:
    """Prepara il database e mostra il menu finché l'utente non esce."""
    # Prima verifica: solo il server, il database potrebbe non esistere ancora
    if not verifica_connessione(None):
        sys.exit(1)
    try:
        inizializza()
        print(f"[DATABASE] '{NOME_DB}' pronto (tabelle e categorie predefinite create se mancanti)")
    except Error as errore:
        print(f"[ERRORE] MySQL: {errore}")
        sys.exit(1)
    # Seconda verifica: ora la connessione è al database della rubrica
    if not verifica_connessione(NOME_DB):
        sys.exit(1)

    azioni = {
        "1": azione_inserisci,
        "2": azione_elenca,
        "3": azione_dettaglio,
        "4": azione_cerca,
        "5": azione_modifica,
        "6": azione_elimina,
        "7": azione_categorie,
        "8": azione_esporta,
        "9": azione_importa,
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
        # Un errore in una voce non deve chiudere il programma
        try:
            azione()
        except IntegrityError as errore:
            print(f"[ERRORE] Vincolo del database: {errore}")
        except Error as errore:
            print(f"[ERRORE] MySQL: {errore}")
        except OSError as errore:
            print(f"[ERRORE] File: {errore}")


if __name__ == "__main__":
    main()