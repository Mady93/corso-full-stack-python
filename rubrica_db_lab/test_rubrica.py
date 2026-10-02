"""Test automatici della rubrica su un database dedicato (rubrica_test)."""

import os

# Va impostato PRIMA di importare i moduli della rubrica, che leggono RUBRICA_DB all'import
os.environ["RUBRICA_DB"] = "rubrica_test"

import csv
import tempfile
from pathlib import Path

from database.db import apri_connessione
from rubrica_db_lab import categorie, contatti, csv_io, schema
from rubrica_db_lab.config import NOME_DB

# Esito (True/False) di ogni verifica
esiti: list[bool] = []


def controlla(descrizione: str, condizione: bool) -> None:
    """Stampa OK o KO per una verifica e ne memorizza l'esito."""
    esiti.append(bool(condizione))
    print(f"   [{'OK' if condizione else 'KO'}] {descrizione}")


def conta(query: str, parametri: tuple = ()) -> int:
    """Esegue una SELECT COUNT e restituisce il numero."""
    connessione = apri_connessione(NOME_DB)
    cursor = connessione.cursor()
    try:
        cursor.execute(query, parametri)
        return cursor.fetchone()[0]
    finally:
        cursor.close()
        connessione.close()


def elimina_database_di_test() -> None:
    """Elimina il database rubrica_test."""
    connessione = apri_connessione(None)
    cursor = connessione.cursor()
    try:
        cursor.execute(f"DROP DATABASE IF EXISTS {NOME_DB}")
    finally:
        cursor.close()
        connessione.close()


def main() -> None:
    """Esegue i test di inserimento, ricerca, modifica, eliminazione, esportazione e importazione."""
    print(f"=== TEST RUBRICA (database '{NOME_DB}') ===")
    schema.inizializza()
    try:
        cat = {c["nome"]: c["id"] for c in categorie.elenca_categorie()}
        controlla("categorie predefinite create con il batch", len(cat) == 5)

        print("[INSERIMENTO]")
        id1 = contatti.inserisci_contatto(
            "Giulia", "Rossi", "3331112222", "giulia@example.com", "collega", [cat["Lavoro"], cat["Amici"]]
        )
        c1 = contatti.trova_contatto(id1)
        controlla("dati salvati correttamente", c1 and c1["cognome"] == "Rossi" and c1["email"] == "giulia@example.com")
        controlla("due categorie associate", c1 and sorted(c1["categorie"].split("|")) == ["Amici", "Lavoro"])
        id2 = contatti.inserisci_contatto("Marco", "Bianchi", "3334445555", None, None, [cat["Famiglia"]])
        controlla("contatto senza email salvato (NULL)", contatti.trova_contatto(id2)["email"] is None)

        print("[RICERCA]")
        controlla("per cognome parziale", [c["id"] for c in contatti.cerca_contatti({"cognome": "ross"})] == [id1])
        controlla(
            "combinata nome + categoria",
            [c["id"] for c in contatti.cerca_contatti({"nome": "marco", "categoria": "famiglia"})] == [id2],
        )
        controlla("combinazione senza risultati", contatti.cerca_contatti({"nome": "giulia", "categoria": "famiglia"}) == [])
        controlla("per telefono ed email insieme", len(contatti.cerca_contatti({"telefono": "3331", "email": "giulia"})) == 1)

        print("[MODIFICA]")
        contatti.modifica_contatto(id1, {"telefono": "3339998888", "note": "aggiornata"})
        dopo = contatti.trova_contatto(id1)
        controlla("campi modificati nel database", dopo["telefono"] == "3339998888" and dopo["note"] == "aggiornata")
        controlla("campi non toccati invariati", dopo["nome"] == "Giulia" and dopo["email"] == "giulia@example.com")
        contatti.imposta_categorie(id1, [cat["Scuola"]])
        controlla("categorie sostituite", contatti.trova_contatto(id1)["categorie"] == "Scuola")
        contatti.imposta_categorie(id1, [cat["Lavoro"], cat["Amici"]])

        print("[ELIMINAZIONE]")
        controlla("rowcount = 1", contatti.elimina_contatto(id2) == 1)
        controlla("contatto non esiste più", contatti.trova_contatto(id2) is None)
        controlla(
            "legami con le categorie eliminati (CASCADE)",
            conta("SELECT COUNT(*) FROM contatti_categorie WHERE contatto_id = %s", (id2,)) == 0,
        )
        controlla("eliminare un id inesistente: rowcount = 0", contatti.elimina_contatto(id2) == 0)

        with tempfile.TemporaryDirectory() as cartella:
            print("[ESPORTAZIONE]")
            file_export = Path(cartella) / "rubrica.csv"
            controlla("1 contatto esportato", csv_io.esporta_csv(file_export) == 1)
            with open(file_export, newline="", encoding="utf-8-sig") as f:
                righe = list(csv.DictReader(f, delimiter=";"))
            controlla("contenuto del file corretto", righe[0]["email"] == "giulia@example.com")
            controlla("categorie nel file", sorted(righe[0]["categorie"].split("|")) == ["Amici", "Lavoro"])

            print("[IMPORTAZIONE]")
            file_import = Path(cartella) / "import.csv"
            with open(file_import, "w", newline="", encoding="utf-8-sig") as f:
                scrittore = csv.DictWriter(f, fieldnames=csv_io.COLONNE, delimiter=";")
                scrittore.writeheader()
                scrittore.writerows([
                    {"nome": "Luca", "cognome": "Verdi", "telefono": "3330001111", "email": "luca@example.com", "note": "", "categorie": "Amici|Palestra"},
                    {"nome": "Anna", "cognome": "Neri", "telefono": "", "email": "anna@example.com", "note": "", "categorie": ""},
                    {"nome": "Giulia", "cognome": "Rossi", "telefono": "", "email": "giulia@example.com", "note": "", "categorie": ""},
                    {"nome": "", "cognome": "SenzaNome", "telefono": "3330002222", "email": "", "note": "", "categorie": ""},
                ])
            r = csv_io.importa_csv(file_import)
            controlla("righe lette = 4", r["letti"] == 4)
            controlla("contatti importati = 2", r["importati"] == 2)
            controlla("duplicati saltati = 1", r["duplicati"] == 1)
            controlla("righe non valide = 1", r["non_validi"] == 1)
            controlla("totale contatti nel database = 3", len(contatti.elenca_contatti()) == 3)
            controlla(
                "categoria nuova creata e associata",
                [c["nome"] for c in contatti.cerca_contatti({"categoria": "palestra"})] == ["Luca"],
            )
            # Reimportare lo stesso file: tutti i contatti validi diventano duplicati
            r2 = csv_io.importa_csv(file_import)
            controlla("secondo import: nessun nuovo contatto", r2["importati"] == 0 and r2["duplicati"] == 3)

        print(f"[RIEPILOGO] test superati: {sum(esiti)}/{len(esiti)}")
    finally:
        # Elimina sempre il database di test, anche se un test fallisce con un errore
        elimina_database_di_test()
        print(f"[PULIZIA] database '{NOME_DB}' eliminato")


if __name__ == "__main__":
    main()