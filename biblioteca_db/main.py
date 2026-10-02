"""Esercizio biblioteca: crea la tabella libri ed esegue il CRUD su MySQL con verifica dei risultati."""

# Serve per fermare il programma con sys.exit
import sys
# Classe base degli errori di MySQL
from mysql.connector import Error
# Funzione che prova la connessione e stampa l'esito (True/False)
from database.db import verifica_connessione
# Funzione che crea la tabella libri se non esiste
from biblioteca_db.schema import crea_tabella
# Funzioni CRUD sulla tabella libri
from biblioteca_db.libri import (
    inserisci_libro,
    elenca_libri,
    libri_dal_anno,
    trova_libro,
    modifica_anno,
    elimina_libro,
    cerca_per_autore
)

# Lista che raccoglie l'esito (True/False) di ogni verifica
esiti: list[bool] = []


def controlla(descrizione: str, condizione: bool) -> None:
    """Stampa OK o KO per una verifica e ne memorizza l'esito."""
    # Salva l'esito per il riepilogo finale
    esiti.append(condizione)
    # Stampa OK se la condizione è vera, KO altrimenti
    print(f"   [VERIFICA {'OK' if condizione else 'KO'}] {descrizione}")


def main() -> None:
    """Verifica la connessione, esegue INSERT, SELECT, UPDATE e DELETE e controlla ogni risultato."""
    # Controlla la connessione: se fallisce, il programma si ferma subito
    if not verifica_connessione():
        sys.exit(1)

    # Se un'operazione dà errore MySQL, salta nell'except
    try:
        # Crea la tabella se non esiste già
        crea_tabella()
        print("[TABELLA] libri pronta")

        # --- INSERT ---
        # Dati del libro da inserire
        titolo: str = "Il nome della rosa"
        autore: str = "Umberto Eco"
        anno: int = 1980
        # Inserisce il libro e ottiene l'id assegnato dal database
        id_nuovo: int = inserisci_libro(titolo, autore, anno)
        print(f"[INSERT] id={id_nuovo} -> {titolo} | {autore} | {anno}")
        # Rilegge il libro dal database e controlla che i dati siano quelli inseriti
        inserito = trova_libro(id_nuovo)
        controlla(
            "il libro esiste con titolo, autore e anno inseriti",
            inserito is not None
            and inserito["titolo"] == titolo
            and inserito["autore"] == autore
            and inserito["anno"] == anno,
        )

        # --- SELECT ---
        print("[SELECT] libri presenti:")
        # Legge tutti i libri e li stampa uno per riga
        libri = elenca_libri()
        for libro in libri:
            print(f"   {libro['id']} - {libro['titolo']} ({libro['autore']}, {libro['anno']})")
        # Controlla che il libro appena inserito compaia nell'elenco
        controlla(
            "il libro inserito compare nell'elenco",
            any(libro["id"] == id_nuovo for libro in libri),
        )

        # --- SELECT con filtro ---
        anno_minimo: int = 1980
        # Inserisce un libro più vecchio del filtro: il filtro deve escluderlo
        id_vecchio: int = inserisci_libro("Il giardino dei Finzi-Contini", "Giorgio Bassani", 1962)
        print(f"[INSERT] id={id_vecchio} -> libro di prova con anno 1962 (sotto il filtro)")
        # Legge solo i libri con anno >= 1980, dal più vecchio al più recente
        filtrati = libri_dal_anno(anno_minimo)
        print(f"[SELECT] libri con anno >= {anno_minimo}:")
        for libro in filtrati:
            print(f"   {libro['id']} - {libro['titolo']} ({libro['autore']}, {libro['anno']})")
        # Controlla che tutti i libri restituiti rispettino il filtro
        controlla(
            f"tutti i libri restituiti hanno anno >= {anno_minimo}",
            all(libro["anno"] >= anno_minimo for libro in filtrati),
        )
        # Il libro del 1980 deve essere incluso (>= include il valore limite)
        controlla(
            "il libro del 1980 è incluso nel filtro",
            any(libro["id"] == id_nuovo for libro in filtrati),
        )
        # Il libro del 1962 deve essere escluso
        controlla(
            "il libro del 1962 è escluso dal filtro",
            all(libro["id"] != id_vecchio for libro in filtrati),
        )
        # Elimina il libro di prova e controlla che sia sparito
        elimina_libro(id_vecchio)
        controlla("il libro di prova è stato eliminato", trova_libro(id_vecchio) is None)

        # --- UPDATE ---
        nuovo_anno: int = 1981
        # Legge il libro prima della modifica per poter stampare il vecchio anno
        prima = trova_libro(id_nuovo)
        # Modifica l'anno: restituisce il numero di righe modificate
        righe_modificate = modifica_anno(id_nuovo, nuovo_anno)
        print(f"[UPDATE] id={id_nuovo} {prima['titolo']}: anno {prima['anno']} -> {nuovo_anno}")
        controlla("l'UPDATE ha modificato esattamente 1 riga", righe_modificate == 1)
        # Rilegge il libro per controllare che l'anno sia cambiato davvero
        dopo = trova_libro(id_nuovo)
        controlla(
            f"l'anno nel database è ora {nuovo_anno}",
            dopo is not None and dopo["anno"] == nuovo_anno,
        )

        # --- SELECT con LIKE ---
        # Cerca i libri il cui autore contiene "Umberto"
        trovati = cerca_per_autore("Umberto")
        print("[SELECT] libri con autore contenente 'Umberto':")
        for libro in trovati:
            print(f"   {libro['id']} - {libro['titolo']} ({libro['autore']}, {libro['anno']})")
        # Il libro di Umberto Eco deve comparire nei risultati
        controlla(
            "la ricerca 'Umberto' trova il libro di Umberto Eco",
            any(libro["id"] == id_nuovo for libro in trovati),
        )
        # Una ricerca senza corrispondenze non deve trovare il libro di Umberto Eco
        controlla(
            "la ricerca 'Bassani' non trova il libro di Umberto Eco",
            all(libro["id"] != id_nuovo for libro in cerca_per_autore("Bassani")),
        )

        # --- DELETE ---
        # Legge il libro prima di eliminarlo per poter stampare cosa viene cancellato
        da_eliminare = trova_libro(id_nuovo)
        # Elimina il libro: restituisce il numero di righe eliminate
        righe_eliminate = elimina_libro(id_nuovo)
        print(f"[DELETE] id={id_nuovo} eliminato -> {da_eliminare['titolo']} | {da_eliminare['autore']} | {da_eliminare['anno']}")
        controlla("il DELETE ha eliminato esattamente 1 riga", righe_eliminate == 1)
        # Rilegge: il libro non deve più esistere
        controlla("il libro non esiste più nel database", trova_libro(id_nuovo) is None)

        # --- RIEPILOGO ---
        print(f"[RIEPILOGO] verifiche superate: {sum(esiti)}/{len(esiti)}")
    # Stampa l'errore MySQL invece di far crashare il programma
    except Error as errore:
        print(f"[ERRORE] MySQL: {errore}")


if __name__ == "__main__":
    main()