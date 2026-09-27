"""
Test manuali sul Core Engine GestionaleJira.

Verifica:
- registrazione utenti
- controllo permessi
- creazione ticket
- duplicati
- ricerca di entita'
- assegnazione ticket
- limite di carico
- avanzamento stato
- commenti
- creazione e gestione Sprint
- integrazione ticket/Sprint
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from eccezioni.eccezioni_custom import (
    DuplicatoError,
    ElementoNonTrovatoError,
    LimiteCaricoLavoroSuperatoError,
    PermessoNegatoError,
    RuoloNonValidoError,
    TicketNonAssegnatoError,
    ValidazioneError,
)
from modelli.configurazione_team import ConfigurazioneTeam
from modelli.sprint import Sprint
from modelli.ticket import BugTicket
from modelli.utente import Utente
from servizi.gestionale_jira import GestionaleJira


class LoggerFinto:
    """Logger usato nei test senza scrittura su file."""

    def __init__(self):
        self.info_messages = []
        self.error_messages = []

    def info(self, messaggio: str) -> None:
        self.info_messages.append(messaggio)

    def error(self, messaggio: str) -> None:
        self.error_messages.append(messaggio)


PERMESSI_DEV = [
    "VIEW_TICKET",
    "COMMENT_TICKET",
    "CHANGE_STATUS",
]

PERMESSI_PM = [
    "VIEW_TICKET",
    "COMMENT_TICKET",
    "CREATE_TICKET",
    "ASSIGN_TICKET",
    "CREATE_SPRINT",
    "MANAGE_SPRINT",
    "MANAGE_TEAM",
]


def crea_ambiente():
    """
    Prepara un GestionaleJira con:
    - un DEV
    - un PM
    - un ticket gia' creato
    """

    jira = GestionaleJira(
        "Progetto Test",
        logger=LoggerFinto(),
    )

    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
        PERMESSI_DEV,
        max_ticket=1,
    )

    pm = Utente(
        "lbianchi",
        "l@test.it",
        "PM",
        PERMESSI_PM,
        dipartimento="Core",
    )

    jira.aggiungi_utente(dev)
    jira.aggiungi_utente(pm)

    bug = BugTicket(
        "BUG-1",
        "Crash login",
        severita="CRITICAL",
    )

    jira.crea_ticket(
        bug,
        "lbianchi",
    )

    return jira, dev, pm, bug


# -------------------------------------- UTENTI --------------------------------------
def test_aggiunta_utente():
    jira = GestionaleJira(
        "Progetto Test",
        logger=LoggerFinto(),
    )

    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
    )

    jira.aggiungi_utente(dev)

    assert len(jira.elenca_utenti()) == 1
    assert jira.elenca_utenti()[0] is dev


def test_utente_duplicato_solleva_eccezione():
    jira, dev, pm, bug = crea_ambiente()

    try:
        jira.aggiungi_utente(
            Utente(
                "mrossi",
                "altro@test.it",
                "DEV",
            )
        )
        assert False
    except DuplicatoError:
        pass


def test_verifica_permesso_utente_autorizzato():
    jira, dev, pm, bug = crea_ambiente()

    jira.verifica_permesso(
        "lbianchi",
        "CREATE_TICKET",
    )


def test_verifica_permesso_negato():
    jira, dev, pm, bug = crea_ambiente()

    try:
        jira.verifica_permesso(
            "mrossi",
            "CREATE_TICKET",
        )
        assert False
    except PermessoNegatoError:
        pass


def test_verifica_permesso_utente_inesistente():
    jira, dev, pm, bug = crea_ambiente()

    try:
        jira.verifica_permesso(
            "sconosciuto",
            "CREATE_TICKET",
        )
        assert False
    except ElementoNonTrovatoError:
        pass


# -------------------------------------- TICKET --------------------------------------
def test_creazione_ticket():
    jira, dev, pm, bug = crea_ambiente()

    secondo_bug = BugTicket(
        "BUG-2",
        "Altro bug",
        severita="MINOR",
    )

    jira.crea_ticket(
        secondo_bug,
        "lbianchi",
    )

    assert jira.cerca_ticket_per_codice("BUG-2") is secondo_bug
    assert len(jira.elenca_ticket()) == 2


def test_creazione_ticket_senza_permesso():
    jira, dev, pm, bug = crea_ambiente()

    nuovo_bug = BugTicket(
        "BUG-2",
        "Altro bug",
        severita="MINOR",
    )

    try:
        jira.crea_ticket(
            nuovo_bug,
            "mrossi",
        )
        assert False
    except PermessoNegatoError:
        pass


def test_ticket_duplicato_solleva_eccezione():
    jira, dev, pm, bug = crea_ambiente()

    try:
        jira.crea_ticket(
            BugTicket(
                "BUG-1",
                "Altro bug",
                severita="MINOR",
            ),
            "lbianchi",
        )
        assert False
    except DuplicatoError:
        pass


def test_cerca_ticket_inesistente():
    jira, dev, pm, bug = crea_ambiente()

    try:
        jira.cerca_ticket_per_codice("BUG-999")
        assert False
    except ElementoNonTrovatoError:
        pass


# -------------------------------------- ASSEGNAZIONE --------------------------------------
def test_assegnazione_normale():
    jira, dev, pm, bug = crea_ambiente()

    jira.assegna_ticket(
        "BUG-1",
        "mrossi",
        "lbianchi",
    )

    assert bug.assegnatario is dev
    assert dev.ticket_in_carico == 1


def test_assegna_ticket_inesistente():
    jira, dev, pm, bug = crea_ambiente()

    try:
        jira.assegna_ticket(
            "BUG-999",
            "mrossi",
            "lbianchi",
        )
        assert False
    except ElementoNonTrovatoError:
        pass


def test_assegna_a_utente_inesistente():
    jira, dev, pm, bug = crea_ambiente()

    try:
        jira.assegna_ticket(
            "BUG-1",
            "sconosciuto",
            "lbianchi",
        )
        assert False
    except ElementoNonTrovatoError:
        pass


def test_assegna_ticket_a_project_manager_non_per_messo():
    jira, dev, pm, bug = crea_ambiente()

    try:
        jira.assegna_ticket(
            "BUG-1",
            "lbianchi",
            "lbianchi",
        )
        assert False
    except RuoloNonValidoError:
        pass


def test_assegna_ticket_senza_permesso():
    jira, dev, pm, bug = crea_ambiente()

    try:
        jira.assegna_ticket(
            "BUG-1",
            "mrossi",
            "mrossi",
        )
        assert False
    except PermessoNegatoError:
        pass


def test_assegna_ticket_gia_assegnato():
    jira, dev, pm, bug = crea_ambiente()

    jira.assegna_ticket(
        "BUG-1",
        "mrossi",
        "lbianchi",
    )

    try:
        jira.assegna_ticket(
            "BUG-1",
            "mrossi",
            "lbianchi",
        )
        assert False
    except DuplicatoError:
        pass


# -------------------------------------- LIMITE DI CARICO --------------------------------------
def test_limite_carico_di_lavoro_superato():
    jira, dev, pm, bug = crea_ambiente()

    secondo_bug = BugTicket(
        "BUG-2",
        "Altro bug",
        severita="MINOR",
    )

    jira.crea_ticket(
        secondo_bug,
        "lbianchi",
    )

    jira.assegna_ticket(
        "BUG-1",
        "mrossi",
        "lbianchi",
    )

    try:
        jira.assegna_ticket(
            "BUG-2",
            "mrossi",
            "lbianchi",
        )
        assert False
    except LimiteCaricoLavoroSuperatoError:
        pass


# -------------------------------------- AVANZAMENTO STATO --------------------------------------
def test_avanza_stato_ticket():
    jira, dev, pm, bug = crea_ambiente()

    jira.assegna_ticket(
        "BUG-1",
        "mrossi",
        "lbianchi",
    )

    jira.avanza_stato_ticket(
        "BUG-1",
        "IN_PROGRESS",
        "mrossi",
    )

    assert bug.stato == "IN_PROGRESS"


def test_avanza_stato_ticket_da_utente_non_assegnatario():
    jira, dev, pm, bug = crea_ambiente()

    altro_dev = Utente(
        "gverdi",
        "g@test.it",
        "DEV",
        PERMESSI_DEV,
        max_ticket=2,
    )

    jira.aggiungi_utente(altro_dev)

    jira.assegna_ticket(
        "BUG-1",
        "mrossi",
        "lbianchi",
    )

    try:
        jira.avanza_stato_ticket(
            "BUG-1",
            "IN_PROGRESS",
            "gverdi",
        )
        assert False
    except RuoloNonValidoError:
        pass


def test_avanza_stato_ticket_non_assegnato():
    jira, dev, pm, bug = crea_ambiente()

    try:
        jira.avanza_stato_ticket(
            "BUG-1",
            "IN_PROGRESS",
            "mrossi",
        )
        assert False
    except TicketNonAssegnatoError:
        pass


def test_ticket_done_decrementa_carico():
    jira, dev, pm, bug = crea_ambiente()

    jira.assegna_ticket(
        "BUG-1",
        "mrossi",
        "lbianchi",
    )

    assert dev.ticket_in_carico == 1

    jira.avanza_stato_ticket(
        "BUG-1",
        "IN_PROGRESS",
        "mrossi",
    )

    jira.avanza_stato_ticket(
        "BUG-1",
        "IN_REVIEW",
        "mrossi",
    )

    jira.avanza_stato_ticket(
        "BUG-1",
        "DONE",
        "mrossi",
    )

    assert bug.stato == "DONE"
    assert dev.ticket_in_carico == 0

    # DONE -> DONE e' consentito,
    # ma non deve diminuire nuovamente il carico.
    jira.avanza_stato_ticket(
        "BUG-1",
        "DONE",
        "mrossi",
    )

    assert dev.ticket_in_carico == 0

# -------------------------------------- COMMENTI --------------------------------------
def test_aggiungi_commento_ticket():
    jira, dev, pm, bug = crea_ambiente()

    jira.aggiungi_commento_ticket(
        "BUG-1",
        "lbianchi",
        "Sto verificando il problema",
    )

    assert len(bug.commenti) == 1
    assert "lbianchi" in bug.commenti[0]
    assert "Sto verificando il problema" in bug.commenti[0]


def test_aggiungi_commento_ticket_inesistente():
    jira, dev, pm, bug = crea_ambiente()

    try:
        jira.aggiungi_commento_ticket(
            "BUG-999",
            "lbianchi",
            "Commento",
        )
        assert False
    except ElementoNonTrovatoError:
        pass


# -------------------------------------- SPRINT --------------------------------------
def test_creazione_sprint():
    jira, dev, pm, bug = crea_ambiente()

    sprint = Sprint(
        "Sprint 1",
        "Obiettivo",
    )

    jira.crea_sprint(
        sprint,
        "lbianchi",
    )

    assert jira.cerca_sprint_per_nome("Sprint 1") is sprint
    assert len(jira.elenca_sprint()) == 1


def test_creazione_sprint_duplicato():
    jira, dev, pm, bug = crea_ambiente()

    jira.crea_sprint(
        Sprint("Sprint 1", "Obiettivo"),
        "lbianchi",
    )

    try:
        jira.crea_sprint(
            Sprint("Sprint 1", "Altro obiettivo"),
            "lbianchi",
        )
        assert False
    except DuplicatoError:
        pass


def test_creazione_sprint_senza_permesso():
    jira, dev, pm, bug = crea_ambiente()

    try:
        jira.crea_sprint(
            Sprint("Sprint 1", "Obiettivo"),
            "mrossi",
        )
        assert False
    except PermessoNegatoError:
        pass


def test_cerca_sprint_inesistente():
    jira, dev, pm, bug = crea_ambiente()

    try:
        jira.cerca_sprint_per_nome("Sprint Fantasma")
        assert False
    except ElementoNonTrovatoError:
        pass


# -------------------------------------- INTEGRAZIONE TICKET / SPRINT --------------------------------------
def test_ticket_aggiunto_a_sprint():
    jira, dev, pm, bug = crea_ambiente()

    jira.crea_sprint(
        Sprint("Sprint 1", "Obiettivo"),
        "lbianchi",
    )

    jira.aggiungi_ticket_a_sprint(
        "Sprint 1",
        "BUG-1",
        "lbianchi",
    )

    sprint = jira.cerca_sprint_per_nome("Sprint 1")

    assert len(sprint.elenca_ticket()) == 1
    assert sprint.elenca_ticket()[0] is bug


def test_aggiungi_ticket_a_sprint_inesistente():
    jira, dev, pm, bug = crea_ambiente()

    try:
        jira.aggiungi_ticket_a_sprint(
            "Sprint Fantasma",
            "BUG-1",
            "lbianchi",
        )
        assert False
    except ElementoNonTrovatoError:
        pass


def test_aggiungi_ticket_inesistente_a_sprint():
    jira, dev, pm, bug = crea_ambiente()

    jira.crea_sprint(
        Sprint("Sprint 1", "Obiettivo"),
        "lbianchi",
    )

    try:
        jira.aggiungi_ticket_a_sprint(
            "Sprint 1",
            "BUG-999",
            "lbianchi",
        )
        assert False
    except ElementoNonTrovatoError:
        pass


def test_ticket_non_puo_stare_in_due_sprint():
    jira, dev, pm, bug = crea_ambiente()

    jira.crea_sprint(
        Sprint("Sprint 1", "Obiettivo 1"),
        "lbianchi",
    )

    jira.crea_sprint(
        Sprint("Sprint 2", "Obiettivo 2"),
        "lbianchi",
    )

    jira.aggiungi_ticket_a_sprint(
        "Sprint 1",
        "BUG-1",
        "lbianchi",
    )

    try:
        jira.aggiungi_ticket_a_sprint(
            "Sprint 2",
            "BUG-1",
            "lbianchi",
        )
        assert False
    except DuplicatoError:
        pass


def test_avvia_sprint():
    jira, dev, pm, bug = crea_ambiente()

    jira.crea_sprint(
        Sprint("Sprint 1", "Obiettivo"),
        "lbianchi",
    )

    jira.avvia_sprint(
        "Sprint 1",
        "lbianchi",
    )

    sprint = jira.cerca_sprint_per_nome("Sprint 1")

    assert sprint.attivo


def test_chiudi_sprint():
    jira, dev, pm, bug = crea_ambiente()

    jira.crea_sprint(
        Sprint("Sprint 1", "Obiettivo"),
        "lbianchi",
    )

    jira.avvia_sprint(
        "Sprint 1",
        "lbianchi",
    )

    jira.chiudi_sprint(
        "Sprint 1",
        "lbianchi",
    )

    sprint = jira.cerca_sprint_per_nome("Sprint 1")

    assert not sprint.attivo


# -------------------------------------- LIMITE TEAM --------------------------------------
def test_imposta_limite_ticket_team():
    jira, dev, pm, bug = crea_ambiente()

    jira.imposta_limite_ticket_team(
        5,
        "lbianchi",
    )

    assert jira.limite_ticket_dev == 5
    assert dev.max_ticket == 5


def test_imposta_limite_ticket_team_negativo():
    jira, dev, pm, bug = crea_ambiente()

    try:
        jira.imposta_limite_ticket_team(
            -1,
            "lbianchi",
        )
        assert False
    except ValidazioneError:
        pass


def test_imposta_limite_team_senza_permesso():
    jira, dev, pm, bug = crea_ambiente()

    try:
        jira.imposta_limite_ticket_team(
            5,
            "mrossi",
        )
        assert False
    except PermessoNegatoError:
        pass


# -------------------------------------- ESECUZIONE DIRETTA DEL FILE --------------------------------------

if __name__ == "__main__":
    funzioni = [
        v
        for k, v in list(globals().items())
        if k.startswith("test_") and callable(v)
    ]

    for f in funzioni:
        f()
        print(f"[OK] {f.__name__}")

    print(f"\n{len(funzioni)} test superati.")