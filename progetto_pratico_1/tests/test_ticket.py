"""
Test manuali sul modulo Ticket.

Verifica:
- creazione e proprieta'
- stato iniziale
- assegnazione
- avanzamento del workflow
- transizioni non valide
- commenti
- storico
- complessita' polimorfica
- rappresentazione testuale
- BugTicket e FeatureTicket
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from eccezioni.eccezioni_custom import (
    TicketNonAssegnatoError,
    TransizioneStatoNonValidaError,
)
from modelli.ticket import Ticket, BugTicket, FeatureTicket
from modelli.utente import Utente


# ---------------------------- CREAZIONE E PROPRIETA' ----------------------------
def test_creazione_ticket_stato_iniziale_todo():
    bug = BugTicket(
        "BUG-1",
        "Crash al login",
        severita="CRITICAL",
    )

    assert bug.codice == "BUG-1"
    assert bug.titolo == "Crash al login"
    assert bug.stato == "TODO"
    assert bug.priorita == "ALTA"
    assert bug.assegnatario is None


def test_creazione_ticket_base():
    ticket = Ticket(
        "TCK-1",
        "Ticket generico",
        priorita="BASSA",
    )

    assert ticket.codice == "TCK-1"
    assert ticket.titolo == "Ticket generico"
    assert ticket.priorita == "BASSA"
    assert ticket.stato == "TODO"
    assert ticket.assegnatario is None


def test_priorita_convertita_in_maiuscolo():
    ticket = Ticket(
        "TCK-1",
        "Ticket generico",
        priorita="media",
    )

    assert ticket.priorita == "MEDIA"


# ---------------------------- ASSEGNAZIONE ----------------------------
def test_assegnazione_sviluppatore():
    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
        ["CHANGE_STATUS"],
        max_ticket=2,
    )

    bug = BugTicket(
        "BUG-1",
        "Crash al login",
        severita="CRITICAL",
    )

    bug.assegnatario = dev

    assert bug.assegnatario == dev
    assert bug.assegnatario.username == "mrossi"


def test_storico_registra_assegnazione():
    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
        [],
        max_ticket=2,
    )

    bug = BugTicket(
        "BUG-1",
        "Crash al login",
        severita="CRITICAL",
    )

    bug.assegnatario = dev

    assert len(bug.storico) == 2
    assert "Assegnato a mrossi" in bug.storico[-1]


# ---------------------------- AVANZAMENTO STATO ----------------------------
def test_avanzamento_normale_dopo_assegnazione():
    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
        ["CHANGE_STATUS"],
        max_ticket=2,
    )

    bug = BugTicket(
        "BUG-1",
        "Crash al login",
        severita="CRITICAL",
    )

    bug.assegnatario = dev
    bug.avanza_stato("IN_PROGRESS")

    assert bug.stato == "IN_PROGRESS"


def test_avanzamento_completo():
    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
        ["CHANGE_STATUS"],
        max_ticket=2,
    )

    bug = BugTicket(
        "BUG-1",
        "Crash al login",
        severita="CRITICAL",
    )

    bug.assegnatario = dev

    bug.avanza_stato("IN_PROGRESS")
    assert bug.stato == "IN_PROGRESS"

    bug.avanza_stato("IN_REVIEW")
    assert bug.stato == "IN_REVIEW"

    bug.avanza_stato("DONE")
    assert bug.stato == "DONE"


def test_avanzamento_accetta_stato_minuscolo():
    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
        [],
        max_ticket=2,
    )

    bug = BugTicket(
        "BUG-1",
        "Crash al login",
        severita="CRITICAL",
    )

    bug.assegnatario = dev
    bug.avanza_stato("in_progress")

    assert bug.stato == "IN_PROGRESS"


# ---------------------------- CASI LIMITE E TRANSIZIONI NON VALIDE ----------------------------
def test_avanzamento_senza_assegnatario_solleva_eccezione():
    bug = BugTicket(
        "BUG-1",
        "Crash al login",
        severita="CRITICAL",
    )

    try:
        bug.avanza_stato("IN_PROGRESS")
        assert False
    except TicketNonAssegnatoError:
        pass


def test_salto_di_stato_vietato():
    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
        [],
        max_ticket=2,
    )

    bug = BugTicket(
        "BUG-1",
        "Crash al login",
        severita="CRITICAL",
    )

    bug.assegnatario = dev

    try:
        bug.avanza_stato("DONE")
        assert False
    except TransizioneStatoNonValidaError:
        pass


def test_stato_non_riconosciuto():
    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
        [],
        max_ticket=2,
    )

    bug = BugTicket(
        "BUG-1",
        "Crash al login",
        severita="CRITICAL",
    )

    bug.assegnatario = dev

    try:
        bug.avanza_stato("ARCHIVIATO")
        assert False
    except TransizioneStatoNonValidaError:
        pass


def test_done_done_e_tollerato():
    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
        [],
        max_ticket=2,
    )

    bug = BugTicket(
        "BUG-1",
        "Crash al login",
        severita="CRITICAL",
    )

    bug.assegnatario = dev

    bug.avanza_stato("IN_PROGRESS")
    bug.avanza_stato("IN_REVIEW")
    bug.avanza_stato("DONE")
    bug.avanza_stato("DONE")

    assert bug.stato == "DONE"


def test_todo_todo_non_avanza():
    bug = BugTicket(
        "BUG-1",
        "Crash al login",
        severita="CRITICAL",
    )

    try:
        bug.avanza_stato("TODO")
        assert False
    except TransizioneStatoNonValidaError:
        pass


# ---------------------------- STORICO ----------------------------
def test_storico_creazione_ticket():
    bug = BugTicket(
        "BUG-1",
        "Crash al login",
        severita="CRITICAL",
    )

    assert len(bug.storico) == 1
    assert "Creazione Ticket" in bug.storico[0]
    assert "Sistema" in bug.storico[0]


def test_storico_cambio_stato():
    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
        [],
        max_ticket=2,
    )

    bug = BugTicket(
        "BUG-1",
        "Crash al login",
        severita="CRITICAL",
    )

    bug.assegnatario = dev
    bug.avanza_stato("IN_PROGRESS")

    assert "Cambio stato: TODO -> IN_PROGRESS" in bug.storico[-1]


def test_storico_restituisce_copia():
    bug = BugTicket(
        "BUG-1",
        "Crash al login",
        severita="CRITICAL",
    )

    storico = bug.storico
    storico.append("modifica esterna")

    assert "modifica esterna" not in bug.storico


# ---------------------------- COMMENTI ----------------------------
def test_aggiungi_commento():
    bug = BugTicket(
        "BUG-1",
        "Crash al login",
        severita="CRITICAL",
    )

    bug.aggiungi_commento(
        "mrossi",
        "Sto indagando",
    )

    assert len(bug.commenti) == 1
    assert "mrossi" in bug.commenti[0]
    assert "Sto indagando" in bug.commenti[0]


def test_commenti_restituiscono_copia():
    bug = BugTicket(
        "BUG-1",
        "Crash al login",
        severita="CRITICAL",
    )

    bug.aggiungi_commento(
        "mrossi",
        "Commento",
    )

    commenti = bug.commenti
    commenti.append("modifica esterna")

    assert len(bug.commenti) == 1


# ---------------------------- BUGTICKET ----------------------------
def test_bug_severita_convertita_in_maiuscolo():
    bug = BugTicket(
        "BUG-1",
        "Crash al login",
        severita="critical",
    )

    assert bug.severita == "CRITICAL"


def test_calcola_complessita_bug_critico():
    bug = BugTicket(
        "BUG-1",
        "Crash al login",
        severita="CRITICAL",
    )

    assert bug.calcola_complessita() == "URGENTE - Blocco Critico"


def test_calcola_complessita_bug_blocks():
    bug = BugTicket(
        "BUG-1",
        "Sistema bloccato",
        severita="BLOCKS",
    )

    assert bug.calcola_complessita() == "URGENTE - Blocco Critico"


def test_calcola_complessita_bug_minore():
    bug = BugTicket(
        "BUG-2",
        "Typo",
        severita="MINOR",
    )

    assert bug.calcola_complessita() == "Bugfix Standard"


def test_str_bug():
    bug = BugTicket(
        "BUG-1",
        "Crash al login",
        severita="CRITICAL",
    )

    testo = str(bug)

    assert "[BUG - Severita': CRITICAL]" in testo
    assert "[BUG-1]" in testo
    assert "Crash al login" in testo


# ---------------------------- FEATURETICKET ----------------------------
def test_feature_story_points():
    feature = FeatureTicket(
        "FEA-1",
        "Nuova dashboard",
        story_points=8,
    )

    assert feature.story_points == 8


def test_calcola_complessita_feature_alta():
    feature = FeatureTicket(
        "FEA-1",
        "Nuova dashboard",
        story_points=8,
    )

    assert feature.calcola_complessita() == "Alta Complessita' (8 SP)"


def test_calcola_complessita_feature_molto_alta():
    feature = FeatureTicket(
        "FEA-1",
        "Nuova dashboard",
        story_points=13,
    )

    assert feature.calcola_complessita() == "Alta Complessita' (13 SP)"


def test_calcola_complessita_feature_bassa():
    feature = FeatureTicket(
        "FEA-2",
        "Bottone",
        story_points=2,
    )

    assert feature.calcola_complessita() == "Media/Bassa Complessita' (2 SP)"


def test_calcola_complessita_feature_sotto_otto():
    feature = FeatureTicket(
        "FEA-2",
        "Bottone",
        story_points=7,
    )

    assert feature.calcola_complessita() == "Media/Bassa Complessita' (7 SP)"


def test_str_feature():
    feature = FeatureTicket(
        "FEA-1",
        "Nuova dashboard",
        story_points=8,
    )

    testo = str(feature)

    assert "[FEATURE - 8 SP]" in testo
    assert "[FEA-1]" in testo
    assert "Nuova dashboard" in testo


# ---------------------------- POLIMORFISMO ----------------------------
def test_polimorfismo_calcola_complessita():
    ticket_bug = BugTicket(
        "BUG-1",
        "Crash",
        severita="CRITICAL",
    )

    ticket_feature = FeatureTicket(
        "FEA-1",
        "Dashboard",
        story_points=8,
    )

    assert ticket_bug.calcola_complessita() != ticket_feature.calcola_complessita()


# ---------------------------- ESECUZIONE DIRETTA DEL FILE ----------------------------

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