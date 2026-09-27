"""
Modulo dei Ticket: Ticket (classe base) -> BugTicket / FeatureTicket.

Qui vive la logica di dominio del singolo ticket: stato, storico,
commenti e la regola di avanzamento del workflow. Le due sottoclassi
usano il polimorfismo per personalizzare calcola_complessita() e
__str__() in base al tipo di lavoro (bug vs feature).
"""

from datetime import datetime
import random

from eccezioni.eccezioni_custom import (
    TicketNonAssegnatoError,
    TransizioneStatoNonValidaError,
)

from servizi.logger import FileLogger


STATI_VALIDI = ["TODO", "IN_PROGRESS", "IN_REVIEW", "DONE"]


class Ticket:
    """Classe base per un Ticket di lavoro."""

    def __init__(
        self,
        codice: str,
        titolo: str,
        priorita: str = "MEDIA",
        logger=None
    ) -> None:

        self._codice: str = codice or f"TCK-{random.randint(1, 9999)}"
        self._titolo: str = titolo
        self._priorita: str = priorita.upper()
        self._stato: str = "TODO"
        self._assegnatario = None
        self._commenti: list[str] = []
        self._storico: list[str] = []

        self._registra_storico("Creazione Ticket", "Sistema")

        self._logger = logger if logger is not None else FileLogger()

    @property
    def codice(self) -> str:
        return self._codice

    @property
    def titolo(self) -> str:
        return self._titolo

    @property
    def priorita(self) -> str:
        return self._priorita

    @property
    def stato(self) -> str:
        return self._stato

    @property
    def assegnatario(self):
        return self._assegnatario

    @assegnatario.setter
    def assegnatario(self, sviluppatore) -> None:
        """Assegna lo sviluppatore responsabile del ticket."""

        self._assegnatario = sviluppatore

        username = (
            sviluppatore.username
            if sviluppatore
            else "Unassigned"
        )

        self._registra_storico(
            f"Assegnato a {username}",
            "PM/System"
        )

    @property
    def commenti(self) -> list[str]:
        return list(self._commenti)

    @property
    def storico(self) -> list[str]:
        return list(self._storico)

    def aggiungi_commento(self, autore: str, testo: str) -> None:
        """Aggiunge un commento con timestamp."""

        data_ora = datetime.now().strftime("%d/%m/%Y %H:%M")

        self._commenti.append(
            f"[{data_ora}] {autore}: {testo}"
        )

    def avanza_stato(
        self,
        nuovo_stato: str,
        autore: str = "Sistema"
    ) -> None:
        """
        Fa avanzare il ticket di UN solo stato:

        TODO -> IN_PROGRESS -> IN_REVIEW -> DONE
        """

        nuovo_stato = nuovo_stato.upper()

        # 1. Controllo stato valido
        if nuovo_stato not in STATI_VALIDI:
            raise TransizioneStatoNonValidaError(
                f"Stato '{nuovo_stato}' non riconosciuto."
            )

        # 2. Non si puo' uscire da TODO senza assegnatario
        if (
            self._stato == "TODO"
            and nuovo_stato != "TODO"
            and self._assegnatario is None
        ):
            raise TicketNonAssegnatoError(
                f"Il ticket {self._codice} non puo' avanzare: "
                f"nessuno sviluppatore assegnato. "
                f"Assegnalo prima con l'opzione dedicata."
            )

        idx_attuale = STATI_VALIDI.index(self._stato)
        idx_nuovo = STATI_VALIDI.index(nuovo_stato)

        # 3. Non si possono saltare stati
        #    DONE -> DONE e' consentito
        if (
            idx_nuovo != idx_attuale + 1
            and not (
                idx_attuale == 3
                and idx_nuovo == 3
            )
        ):
            raise TransizioneStatoNonValidaError(
                f"Transizione non permessa da "
                f"{self._stato} a {nuovo_stato}. "
                f"Devi avanzare verso "
                f"{STATI_VALIDI[idx_attuale + 1]}."
            )

        vecchio_stato = self._stato

        self._stato = nuovo_stato

        self._registra_storico(
            f"Cambio stato: "
            f"{vecchio_stato} -> {nuovo_stato}",
            autore
        )

    def _registra_storico(
        self,
        azione: str,
        autore: str
    ) -> None:
        """Aggiunge una riga allo storico interno."""

        now = datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        )

        self._storico.append(
            f"[{now}] ({autore}) {azione}"
        )

    def calcola_complessita(self) -> str:
        """Metodo polimorfico."""

        return "Complessita' Standard"

    def __str__(self) -> str:
        dev = (
            self._assegnatario.username
            if self._assegnatario
            else "Non assegnato"
        )

        return (
            f"[{self._codice}] {self._titolo} | "
            f"Stato: {self._stato} | "
            f"Priorita': {self._priorita} | "
            f"Dev: {dev}"
        )


class BugTicket(Ticket):
    """Ticket per tracciare anomalie/bug."""

    def __init__(
        self,
        codice: str,
        titolo: str,
        severita: str,
        priorita: str = "ALTA"
    ) -> None:

        super().__init__(
            codice,
            titolo,
            priorita
        )

        self._severita: str = severita.upper()

    @property
    def severita(self) -> str:
        return self._severita

    def calcola_complessita(self) -> str:
        """La complessita' del bug dipende dalla severita'."""

        if self._severita in ["BLOCKS", "CRITICAL"]:
            return "URGENTE - Blocco Critico"

        return "Bugfix Standard"

    def __str__(self) -> str:
        base = super().__str__()

        return (
            f"[BUG - Severita': {self._severita}] "
            f"{base}"
        )


class FeatureTicket(Ticket):
    """Ticket per lo sviluppo di nuova funzionalita'."""

    def __init__(
        self,
        codice: str,
        titolo: str,
        story_points: int,
        priorita: str = "MEDIA"
    ) -> None:

        super().__init__(
            codice,
            titolo,
            priorita
        )

        self._story_points: int = story_points

    @property
    def story_points(self) -> int:
        return self._story_points

    def calcola_complessita(self) -> str:
        """La complessita' dipende dagli Story Points."""

        if self._story_points >= 8:
            return (
                f"Alta Complessita' "
                f"({self._story_points} SP)"
            )

        return (
            f"Media/Bassa Complessita' "
            f"({self._story_points} SP)"
        )

    def __str__(self) -> str:
        base = super().__str__()

        return (
            f"[FEATURE - {self._story_points} SP] "
            f"{base}"
        )