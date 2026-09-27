"""
Core Engine del sistema: orchestratore della business logic.

GestionaleJira tiene in RAM utenti, ticket e sprint e applica
le regole di dominio prima di modificare i dati.
"""

import random

from eccezioni.eccezioni_custom import (
    DuplicatoError,
    ElementoNonTrovatoError,
    LimiteCaricoLavoroSuperatoError,
    RuoloNonValidoError,
    TicketNonAssegnatoError,
    PermessoNegatoError,
    ValidazioneError,
)

from modelli.configurazione_team import ConfigurazioneTeam
from servizi.logger import FileLogger


class GestionaleJira:
    """Core Manager del sistema Jira."""

    def __init__(
        self,
        nome_progetto: str,
        utenti: dict = None,
        config_team: ConfigurazioneTeam = None,
        logger=None,
    ) -> None:
        """
        Inizializza un nuovo progetto Jira.

        Gli elementi vengono mantenuti in memoria:
        utenti, ticket e sprint.
        """

        self._nome_progetto: str = nome_progetto
        self._utenti: dict = utenti if utenti is not None else {}
        self._ticket: dict = {}
        self._sprint: dict = {}
        self._config_team: ConfigurazioneTeam = (
            config_team if config_team is not None else ConfigurazioneTeam()
        )
        self._logger = logger if logger is not None else FileLogger()
        self._logger.info(f"Progetto '{nome_progetto}' avviato")

    @property
    def limite_ticket_dev(self) -> int:
        return self._config_team.limite_ticket_dev

    def imposta_limite_ticket_team(
        self,
        nuovo_limite: int,
        autore: str
    ) -> None:
        """
        Cambia il limite di ticket in carico per TUTTI i DEV del team
        (nuovi e gia' registrati). Richiede il permesso MANAGE_TEAM,
        riservato al PM.
        """

        self.verifica_permesso(autore, "MANAGE_TEAM")

        if nuovo_limite < 0:
            raise ValidazioneError(
                "Il limite di ticket non puo' essere negativo"
            )

        self._config_team.limite_ticket_dev = nuovo_limite

        for utente in self._utenti.values():
            if utente.get_ruolo() == "DEV":
                utente.impostare_limite_ticket(nuovo_limite)

        self._logger.info(
            f"Limite ticket team aggiornato a {nuovo_limite} "
            f"da {autore}"
        )

    def aggiungi_utente(
        self,
        utente
    ) -> None:
        """
        Registra un nuovo utente nel progetto.

        La username deve essere unica.
        """

        if utente.username in self._utenti:
            raise DuplicatoError(
                f"L'utente con username "
                f"'{utente.username}' esiste gia'"
            )

        self._utenti[utente.username] = utente

        self._logger.info(
            f"Registrato nuovo utente: "
            f"{utente.username}"
        )


    def verifica_permesso(self, username: str, permesso: str) -> None:
        """
        Verifica che l'utente esista e possieda
        il permesso richiesto.
        """

        if username not in self._utenti:
            raise ElementoNonTrovatoError(
                f"Utente '{username}' "
                f"non registrato"
            )

        utente = self._utenti[username]

        if not utente.ha_permesso(permesso):
            raise PermessoNegatoError(
                f"L'utente '{username}' "
                f"non ha il permesso "
                f"'{permesso}'"
            )



    def crea_ticket(
        self,
        ticket,
        autore: str
    ) -> None:
        """
        Inserisce un nuovo ticket nel sistema.

        Se il codice non viene fornito,
        genera automaticamente un codice TCK-XXXX.
        """

        self.verifica_permesso(
            autore,
            "CREATE_TICKET"
        )

        if not ticket.codice:
            numero = random.randint(1, 9999)

            while f"TCK-{numero}" in self._ticket:
                numero = random.randint(1, 9999)

            ticket._codice = f"TCK-{numero}"

        if ticket.codice in self._ticket:
            raise DuplicatoError(
                f"Ticket con codice "
                f"'{ticket.codice}' gia' presente"
            )

        self._ticket[ticket.codice] = ticket

        self._logger.info(
            f"Creato nuovo ticket: "
            f"{ticket.codice}"
        )



    def crea_sprint(
        self,
        sprint,
        autore: str
    ) -> None:
        """
        Registra un nuovo sprint.

        Ogni sprint deve avere un nome unico.
        """

        self.verifica_permesso(
        autore,
        "CREATE_SPRINT"
        )

        if sprint.nome in self._sprint:
            raise DuplicatoError(
                f"Sprint '{sprint.nome}' gia' esistente"
            )

        self._sprint[sprint.nome] = sprint

        self._logger.info(
            f"Creato nuovo Sprint: "
            f"{sprint.nome}"
        )

    def assegna_ticket(
        self,
        codice_ticket: str,
        username_dev: str,
        autore: str
    ) -> None:
        """
        Assegna un ticket ad uno sviluppatore.

        Regole:
        - il ticket deve esistere
        - l'utente deve esistere
        - deve essere uno sviluppatore
        - deve avere spazio disponibile
        - il ticket non deve essere già assegnato
        """

        self.verifica_permesso(
        autore,
        "ASSIGN_TICKET"
        )
        
        if codice_ticket not in self._ticket:
            raise ElementoNonTrovatoError(
                f"Ticket '{codice_ticket}' non trovato"
            )

        if username_dev not in self._utenti:
            raise ElementoNonTrovatoError(
                f"Utente '{username_dev}' "
                f"non registrato"
            )

        dev = self._utenti[username_dev]
        ticket = self._ticket[codice_ticket]

        if ticket.assegnatario is not None:
            raise DuplicatoError(
                f"Il ticket '{codice_ticket}' "
                f"e' gia' assegnato a "
                f"{ticket.assegnatario.username}"
            )

        if dev.get_ruolo() != "DEV":
            raise RuoloNonValidoError(
                f"L'utente '{username_dev}' "
                f"non e' uno sviluppatore"
            )

        if not dev.puo_accettare_ticket():
            raise LimiteCaricoLavoroSuperatoError(
                f"Sviluppatore '{username_dev}' saturo! "
                f"Ha raggiunto il limite di "
                f"{dev.max_ticket} ticket"
            )

        ticket.assegnatario = dev
        dev.incrementa_ticket()

        self._logger.info(
            f"Ticket {codice_ticket} "
            f"assegnato a {username_dev}"
        )

    def avanza_stato_ticket(
        self,
        codice_ticket: str,
        nuovo_stato: str,
        autore: str
    ) -> None:
        """
        Cambia lo stato di un ticket.

        Solo lo sviluppatore assegnatario
        può modificare il workflow.
        """
        self.verifica_permesso(
        autore,
        "CHANGE_STATUS"
        )

        if codice_ticket not in self._ticket:
            raise ElementoNonTrovatoError(
                f"Ticket '{codice_ticket}' "
                f"non trovato"
            )

        if autore not in self._utenti:
            raise ElementoNonTrovatoError(
                f"Utente '{autore}' "
                f"non registrato"
            )

        ticket = self._ticket[codice_ticket]

        if ticket.assegnatario is None:
            raise TicketNonAssegnatoError(
                f"Il ticket '{codice_ticket}' "
                f"non e' assegnato a nessuno"
            )

        if ticket.assegnatario.username != autore:
            raise RuoloNonValidoError(
                f"Il ticket '{codice_ticket}' "
                f"e' assegnato a "
                f"{ticket.assegnatario.username}, "
                f"non a '{autore}'"
            )

        stato_precedente = ticket.stato

        ticket.avanza_stato(
            nuovo_stato,
            autore
        )

        if (
            stato_precedente != "DONE"
            and nuovo_stato.upper() == "DONE"
            and ticket.assegnatario
        ):
            ticket.assegnatario.decrementa_ticket()

        self._logger.info(
            f"Ticket {codice_ticket}: "
            f"{stato_precedente} -> "
            f"{ticket.stato}"
        )


    def aggiungi_ticket_a_sprint(
        self,
        nome_sprint: str,
        codice_ticket: str,
        autore: str
    ) -> None:
        """
        Aggiunge un ticket ad uno sprint.

        Regole:
        - lo sprint deve esistere
        - il ticket deve esistere
        - l'utente deve avere il permesso MANAGE_SPRINT
        """

        self.verifica_permesso(
            autore,
            "MANAGE_SPRINT"
        )

        if nome_sprint not in self._sprint:
            raise ElementoNonTrovatoError(
                f"Sprint '{nome_sprint}' "
                f"non trovato"
            )

        if codice_ticket not in self._ticket:
            raise ElementoNonTrovatoError(
                f"Ticket '{codice_ticket}' "
                f"non trovato"
            )

        sprint = self._sprint[nome_sprint]
        ticket = self._ticket[codice_ticket]

        # Un ticket puo' appartenere ad un solo sprint alla volta,
        # come in Jira reale.
        for altro_nome, altro_sprint in self._sprint.items():
            if altro_nome == nome_sprint:
                continue

            if any(
                t.codice == codice_ticket
                for t in altro_sprint.elenca_ticket()
            ):
                raise DuplicatoError(
                    f"Il ticket '{codice_ticket}' e' gia' presente "
                    f"nello Sprint '{altro_nome}'"
                )

        sprint.aggiungi_ticket(ticket)

        self._logger.info(
            f"Ticket {codice_ticket} "
            f"aggiunto allo Sprint {nome_sprint}"
        )

 
    def cerca_ticket_per_codice(
        self,
        codice_ticket: str
    ):
        """
        Cerca un ticket tramite il suo codice.
        """

        if codice_ticket not in self._ticket:
            raise ElementoNonTrovatoError(
                f"Ticket '{codice_ticket}' "
                f"non trovato"
            )

        return self._ticket[codice_ticket]


    def cerca_sprint_per_nome(
        self,
        nome_sprint: str
    ):
        """
        Cerca uno sprint tramite il suo nome.
        """

        if nome_sprint not in self._sprint:
            raise ElementoNonTrovatoError(
                f"Sprint '{nome_sprint}' "
                f"non trovato"
            )

        return self._sprint[nome_sprint]


    def elenca_utenti(self) -> list:
        """
        Restituisce tutti gli utenti registrati nel progetto.
        """
        return list(self._utenti.values())


    def elenca_ticket(self) -> list:
        """
        Restituisce tutti i ticket presenti in memoria.
        """
        return list(self._ticket.values())


    def elenca_sprint(self) -> list:
        """
        Restituisce tutti gli sprint presenti in memoria.
        """
        return list(self._sprint.values())


    def aggiungi_commento_ticket(
        self,
        codice_ticket: str,
        autore: str,
        testo: str
    ) -> None:
        """
        Aggiunge un commento ad un ticket.
        """

        self.verifica_permesso(
            autore,
            "COMMENT_TICKET"
        )

        if codice_ticket not in self._ticket:
            raise ElementoNonTrovatoError(
                f"Ticket '{codice_ticket}' non trovato"
            )

        ticket = self._ticket[codice_ticket]

        ticket.aggiungi_commento(
            autore,
            testo
        )

        self._logger.info(
            f"Commento aggiunto al ticket "
            f"{codice_ticket}"
        )


    def avvia_sprint(
        self,
        nome_sprint: str,
        autore: str
    ) -> None:
        """
        Avvia uno sprint.

        Richiede il permesso MANAGE_SPRINT.
        """

        self.verifica_permesso(
            autore,
            "MANAGE_SPRINT"
        )

        sprint = self.cerca_sprint_per_nome(
            nome_sprint
        )

        sprint.avvia_sprint()

        self._logger.info(
            f"Sprint '{nome_sprint}' avviato da {autore}"
        )


    def chiudi_sprint(
        self,
        nome_sprint: str,
        autore: str
    ) -> None:
        """
        Chiude uno sprint.

        Richiede il permesso MANAGE_SPRINT.
        """

        self.verifica_permesso(
            autore,
            "MANAGE_SPRINT"
        )

        sprint = self.cerca_sprint_per_nome(
            nome_sprint
        )

        sprint.chiudi_sprint()

        self._logger.info(
            f"Sprint '{nome_sprint}' chiuso da {autore}"
        )


    def registra_errore(
        self,
        messaggio: str
    ) -> None:
        """
        Registra un errore nel log.
        """

        self._logger.error(
            messaggio
        )