"""
Modulo Sprint: gestione dello Sprint e del relativo backlog in RAM.
"""

from eccezioni.eccezioni_custom import StatoSprintError


class Sprint:
    """Rappresenta uno Sprint di lavoro attivabile dal Project Manager."""

    def __init__(self, nome: str, obiettivo: str) -> None:
        self._nome: str = nome
        self._obiettivo: str = obiettivo
        self._ticket_list: list = []
        self._attivo: bool = False

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def obiettivo(self) -> str:
        return self._obiettivo

    @property
    def attivo(self) -> bool:
        return self._attivo

    def avvia_sprint(self) -> None:
        if self._attivo:
            raise StatoSprintError(f"Lo Sprint '{self._nome}' e' gia' attivo")
        self._attivo = True

    def chiudi_sprint(self) -> None:
        if not self._attivo:
            raise StatoSprintError(f"Lo Sprint '{self._nome}' non e' attivo")
        self._attivo = False

    def aggiungi_ticket(self, ticket) -> None:
        # Confronto per codice (chiave di dominio) e non per identita' di
        # oggetto: due riferimenti diversi allo "stesso" ticket devono
        # comunque essere riconosciuti come duplicati.
        if any(t.codice == ticket.codice for t in self._ticket_list):
            raise StatoSprintError(f"Il ticket {ticket.codice} e' gia' presente nello Sprint")
        self._ticket_list.append(ticket)

    def elenca_ticket(self) -> list:
        return list(self._ticket_list)

    def __str__(self) -> str:
        stato_str = "ATTIVO" if self._attivo else "CHIUSO / PIANIFICATO"
        return f"Sprint '{self._nome}' [{stato_str}] | Obiettivo: {self._obiettivo} | Ticket inclusi: {len(self._ticket_list)}"