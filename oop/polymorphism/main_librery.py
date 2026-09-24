"""
Lab sistema biblioteca con ereditarietà
OOP "Parte 1 - Classi e oggetti"

Nessun try/except: ogni operazione rischiosa passa per un metodo
factory (`crea()`) o restituisce True/False/None 
(controlla che i dati siano validi prima di creare l'oggetto;
restituisce None se i dati non sono validi), e il codice controlla
semplicemente il risultato con un `if`.

Questo file copre ESPLICITAMENTE ogni ramo di controllo presente in
validazioni.py e in biblioteca.py (vedi i commenti di sezione).
"""

from library_system.biblioteca import Biblioteca
from library_system.dvd import DVD
from library_system.libro import Libro
from library_system.prestito import Prestito
from library_system.rivista import Rivista
from library_system.utente import Utente


def main() -> None:
    """Create library objects and demonstrate the OOP concepts."""

    # ESERCIZIO 1/2 -- Creazione e gestione di più oggetti.
    library = Biblioteca()

    # Creo tre oggetti di sottoclassi diverse, tramite crea() (nessuna
    # eccezione: se i dati fossero invalidi, crea() stamperebbe l'errore
    # e restituirebbe None).
    book = Libro.crea("The Name of the Rose", "B001", "Umberto Eco", 512)
    magazine = Rivista.crea("National Geographic", "R001", 125, "September")
    dvd = DVD.crea("Inception", "D001", "Christopher Nolan", 148)

    # Creo due utenti.
    user1 = Utente.crea("Mario Rossi", 1)
    user2 = Utente.crea("Laura Bianchi", 2)

    # ESERCIZIO 2 -- Registro materiali e utenti nella biblioteca.
    library.aggiungi_materiale(book)
    library.aggiungi_materiale(magazine)
    library.aggiungi_materiale(dvd)

    library.registra_utente(user1)
    library.registra_utente(user2)

    # ESERCIZIO 6 -- Polimorfismo.
    # Stesso metodo (describe) chiamato su oggetti di classi diverse.
    materials = [book, magazine, dvd]

    print("=== LIBRARY MATERIALS ===")
    for material in materials:
        print(material.describe())
    print()

    # ESERCIZIO 2 -- Effettuo due prestiti validi.
    print("=== LOANS ===")
    for materiale, utente in [(book, user1), (dvd, user2)]:
        loan = Prestito.crea(materiale, utente)
        if loan is not None and library.effettua_prestito(loan):
            print(loan.describe())
    print()

    # ----------------------------------------------------------------
    # effettua_prestito(): copro i 4 rami possibili
    #   A) prestito non è un'istanza di Prestito
    #   B) utente non registrato
    #   C) materiale non registrato
    #   D) materiale già in prestito
    # ----------------------------------------------------------------
    print("=== LOAN BUSINESS RULE CHECKS ===")

    # A) tipo non valido passato direttamente (bypassa Prestito.crea)
    library.effettua_prestito("questo non è un prestito")

    # B) utente non registrato
    unregistered_user = Utente.crea("Luca Verdi", 3)
    loan_b = Prestito.crea(book, unregistered_user)
    if loan_b is not None:
        library.effettua_prestito(loan_b)

    # C) materiale non registrato in biblioteca (mai aggiunto)
    orphan_book = Libro.crea("Orphan Book", "B900", "Nobody", 100)
    loan_c = Prestito.crea(orphan_book, user1)
    if loan_c is not None:
        library.effettua_prestito(loan_c)

    # D) materiale già in prestito (book è già in prestito a user1)
    loan_d = Prestito.crea(book, user2)
    if loan_d is not None:
        library.effettua_prestito(loan_d)
    print()

    # ----------------------------------------------------------------
    # Prestito.crea(): copro i 2 rami possibili
    #   A) materiale non è un'istanza di Materiale
    #   B) utente non è un'istanza di Utente
    # ----------------------------------------------------------------
    print("=== PRESTITO.CREA() TYPE CHECKS ===")
    Prestito.crea("non è un materiale", user1)  # A
    Prestito.crea(book, "non è un utente")      # B
    print()

    # ----------------------------------------------------------------
    # restituisci_materiale(): copro entrambi i rami
    #   A) prestito trovato -> restituito con successo
    #   B) nessun prestito attivo per quel materiale
    # ----------------------------------------------------------------
    print("=== RETURN ===")
    returned = library.restituisci_materiale(book)  # A) successo
    if returned is not None:
        print(f"Returned: {returned.describe()}")

    library.restituisci_materiale(magazine)  # B) mai stato in prestito
    print()

    # ----------------------------------------------------------------
    # testo_valido(): copro i 2 rami
    #   A) il valore non è una stringa
    #   B) la stringa è vuota (o solo spazi)
    # Applicati a campi di classi diverse per coprire ogni chiamata.
    # ----------------------------------------------------------------
    print("=== VALUE CHECKS: testo_valido() ===")
    Libro.crea(123, "B901", "Author", 100)        # A) title non stringa
    Libro.crea("Test", "", "Author", 100)          # B) code vuoto
    Libro.crea("Test", "B902", "", 100)            # B) author vuoto
    Rivista.crea("Test", "R900", 10, "")           # B) month vuoto
    DVD.crea("Test", "D900", "", 100)              # B) director vuoto
    Utente.crea("   ", 10)                         # B) name solo spazi
    print()

    # ----------------------------------------------------------------
    # intero_positivo(): copro i 2 rami (+ trappola dei bool)
    #   A) il valore non è un intero (o è un bool)
    #   B) il valore è <= 0
    # ----------------------------------------------------------------
    print("=== VALUE CHECKS: intero_positivo() ===")
    Libro.crea("Test", "B903", "Author", "cento")  # A) pages non intero
    Libro.crea("Test", "B904", "Author", True)     # A) pages è un bool (trappola)
    Libro.crea("Test", "B905", "Author", 0)        # B) pages = 0
    Libro.crea("Test", "B906", "Author", -10)      # B) pages negativo
    Rivista.crea("Test", "R901", -5, "October")    # B) issue_number negativo
    DVD.crea("Test", "D901", "Director", -120)     # B) duration negativo
    print()

    # ----------------------------------------------------------------
    # intero_non_negativo(): copro i 2 rami (+ trappola dei bool)
    #   A) il valore non è un intero (o è un bool)
    #   B) il valore è < 0
    # ----------------------------------------------------------------
    print("=== VALUE CHECKS: intero_non_negativo() ===")
    Utente.crea("Test User", "dieci")  # A) user_id non intero
    Utente.crea("Test User", True)     # A) user_id è un bool (trappola)
    Utente.crea("Test User", -1)       # B) user_id negativo
    print()

    # ----------------------------------------------------------------
    # aggiungi_materiale() / registra_utente(): copro il ramo "tipo
    # non valido", il ramo "duplicato", e il caso limite in cui si
    # passa None (risultato di una crea() fallita) -- difesa in
    # profondità: anche un None viene bloccato dal controllo di tipo.
    # ----------------------------------------------------------------
    print("=== BIBLIOTECA TYPE & DUPLICATE CHECKS ===")
    library.aggiungi_materiale("non è un materiale")  # tipo non valido
    library.registra_utente("non è un utente")        # tipo non valido

    failed_book = Libro.crea("", "B907", "Author", 100)  # crea() fallisce -> None
    library.aggiungi_materiale(failed_book)                # None bloccato comunque

    duplicate_book = Libro.crea("Duplicate", "B001", "Someone", 100)
    library.aggiungi_materiale(duplicate_book)  # codice duplicato

    duplicate_user = Utente.crea("Duplicate", 1)
    library.registra_utente(duplicate_user)  # ID duplicato
    print()

    # ESERCIZIO 2 -- Consulto lo stato attuale della biblioteca.
    print("=== LIBRARY STATUS ===")
    print(library.descrivi_stato())


if __name__ == "__main__":
    main()