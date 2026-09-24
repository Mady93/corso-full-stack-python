"""Define the library management class
"""

# Ogni operazione "rischiosa" restituisce True/False (o None), stampando
# un messaggio d'errore chiaro quando qualcosa va storto. Nessun
# try/except: il chiamante controlla il risultato con un semplice `if`.

from .materiale import Materiale
from .prestito import Prestito
from .utente import Utente


class Biblioteca:
    """Manage library materials, users, and loans."""

    def __init__(self) -> None:
        """Initialize an empty library."""
        self.materiali = []
        self.utenti = []
        self.prestiti = []

    def aggiungi_materiale(self, materiale) -> bool:
        """Add a material to the library. Returns True on success."""
        if not isinstance(materiale, Materiale):
            print("[Error] Invalid material")
            return False

        # Un materiale reale non deve accettare due codici uguali.
        for m in self.materiali:
            if m.code == materiale.code:
                print(f"[Error] Code '{materiale.code}' is already registered")
                return False

        self.materiali.append(materiale)
        return True

    def registra_utente(self, utente) -> bool:
        """Register a user in the library. Returns True on success."""
        if not isinstance(utente, Utente):
            print("[Error] Invalid user")
            return False

        for u in self.utenti:
            if u.user_id == utente.user_id:
                print(f"[Error] User ID {utente.user_id} is already registered")
                return False

        self.utenti.append(utente)
        return True

    def effettua_prestito(self, prestito) -> bool:
        """Register a loan, after checking every business rule.
        """
        # Ordine dei controlli: prima il tipo (difesa da input non valido),
        # poi "l'utente esiste", poi "il materiale esiste", infine
        # "è disponibile" - dal controllo più generale al più specifico.
        if not isinstance(prestito, Prestito):
            print("[Error] Invalid loan")
            return False

        if prestito.utente not in self.utenti:
            print(f"[Error] User '{prestito.utente.name}' is not registered")
            return False

        if prestito.materiale not in self.materiali:
            print(f"[Error] Material '{prestito.materiale.title}' is not registered")
            return False

        for loan in self.prestiti:
            if loan.materiale is prestito.materiale:
                print(f"[Error] Material '{prestito.materiale.title}' is already on loan")
                return False

        self.prestiti.append(prestito)
        return True

    def restituisci_materiale(self, materiale):

        """Close the active loan for a material and return it, or None."""

        # Chiude (rimuove) il prestito attivo per un materiale, se esiste.
        # Restituisce il Prestito chiuso, oppure None se non c'era nessun
        # prestito attivo per quel materiale.
        for loan in self.prestiti:
            if loan.materiale is materiale:
                self.prestiti.remove(loan)
                return loan
        print(f"[Error] No active loan found for '{materiale.title}'")
        return None

    def descrivi_stato(self) -> str:
        """Return a summary of the current library state."""
        return (
            f"Materials: {len(self.materiali)} | "
            f"Users: {len(self.utenti)} | "
            f"Loans: {len(self.prestiti)}"
        )