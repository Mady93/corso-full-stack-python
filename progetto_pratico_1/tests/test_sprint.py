"""
Test manuali sul modulo Sprint.

Verifica:
- creazione dello Sprint
- proprieta'
- avvio e chiusura
- operazioni ripetute non valide
- gestione del backlog
- duplicazione dei ticket per codice
- restituzione di una copia del backlog
- rappresentazione testuale
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from eccezioni.eccezioni_custom import StatoSprintError
from modelli.sprint import Sprint
from modelli.ticket import FeatureTicket


# ------------------------------ CREAZIONE E PROPRIETA' ------------------------------
def test_sprint_nasce_non_attivo():
    sprint = Sprint(
        "Sprint 1",
        "Rilasciare login",
    )

    assert sprint.nome == "Sprint 1"
    assert sprint.obiettivo == "Rilasciare login"
    assert not sprint.attivo


# ------------------------------ CICLO DI VITA ------------------------------
def test_avvio_sprint():
    sprint = Sprint(
        "Sprint 1",
        "Rilasciare login",
    )

    sprint.avvia_sprint()

    assert sprint.attivo


def test_chiusura_sprint():
    sprint = Sprint(
        "Sprint 1",
        "Rilasciare login",
    )

    sprint.avvia_sprint()
    sprint.chiudi_sprint()

    assert not sprint.attivo


def test_doppio_avvio_solleva_eccezione():
    sprint = Sprint(
        "Sprint 1",
        "Rilasciare login",
    )

    sprint.avvia_sprint()

    try:
        sprint.avvia_sprint()
        assert False
    except StatoSprintError:
        pass


def test_chiusura_sprint_non_attivo_solleva_eccezione():
    sprint = Sprint(
        "Sprint 1",
        "Rilasciare login",
    )

    try:
        sprint.chiudi_sprint()
        assert False
    except StatoSprintError:
        pass


def test_sprint_puo_essere_riavviato_dopo_la_chiusura():
    sprint = Sprint(
        "Sprint 1",
        "Rilasciare login",
    )

    sprint.avvia_sprint()
    sprint.chiudi_sprint()
    sprint.avvia_sprint()

    assert sprint.attivo


# ------------------------------ BACKLOG ------------------------------
def test_aggiungi_ticket():
    sprint = Sprint(
        "Sprint 1",
        "Rilasciare login",
    )

    ticket = FeatureTicket(
        "FEA-1",
        "Login SSO",
        story_points=5,
    )

    sprint.aggiungi_ticket(ticket)

    assert len(sprint.elenca_ticket()) == 1
    assert sprint.elenca_ticket()[0] == ticket


def test_aggiungere_piu_ticket():
    sprint = Sprint(
        "Sprint 1",
        "Rilasciare login",
    )

    ticket1 = FeatureTicket(
        "FEA-1",
        "Login SSO",
        story_points=5,
    )

    ticket2 = FeatureTicket(
        "FEA-2",
        "Dashboard",
        story_points=8,
    )

    sprint.aggiungi_ticket(ticket1)
    sprint.aggiungi_ticket(ticket2)

    assert len(sprint.elenca_ticket()) == 2
    assert sprint.elenca_ticket()[0] == ticket1
    assert sprint.elenca_ticket()[1] == ticket2


def test_aggiungi_ticket_duplicato_solleva_eccezione():
    sprint = Sprint(
        "Sprint 1",
        "Rilasciare login",
    )

    ticket = FeatureTicket(
        "FEA-1",
        "Login SSO",
        story_points=5,
    )

    sprint.aggiungi_ticket(ticket)

    try:
        sprint.aggiungi_ticket(ticket)
        assert False
    except StatoSprintError:
        pass


def test_ticket_con_stesso_codice_e_duplicato():
    sprint = Sprint(
        "Sprint 1",
        "Rilasciare login",
    )

    ticket1 = FeatureTicket(
        "FEA-1",
        "Login SSO",
        story_points=5,
    )

    ticket2 = FeatureTicket(
        "FEA-1",
        "Login SSO diverso",
        story_points=8,
    )

    sprint.aggiungi_ticket(ticket1)

    try:
        sprint.aggiungi_ticket(ticket2)
        assert False
    except StatoSprintError:
        pass


def test_elenca_ticket_vuoto():
    sprint = Sprint(
        "Sprint 1",
        "Rilasciare login",
    )

    assert sprint.elenca_ticket() == []


def test_elenca_ticket_restituisce_copia():
    sprint = Sprint(
        "Sprint 1",
        "Rilasciare login",
    )

    ticket = FeatureTicket(
        "FEA-1",
        "Login SSO",
        story_points=5,
    )

    sprint.aggiungi_ticket(ticket)

    lista = sprint.elenca_ticket()
    lista.clear()

    assert len(sprint.elenca_ticket()) == 1


# ------------------------------ RAPPRESENTAZIONE TESTUALE ------------------------------
def test_str_sprint_non_attivo():
    sprint = Sprint(
        "Sprint 1",
        "Rilasciare login",
    )

    testo = str(sprint)

    assert "Sprint 'Sprint 1'" in testo
    assert "CHIUSO / PIANIFICATO" in testo
    assert "Obiettivo: Rilasciare login" in testo
    assert "Ticket inclusi: 0" in testo


def test_str_sprint_attivo():
    sprint = Sprint(
        "Sprint 1",
        "Rilasciare login",
    )

    sprint.avvia_sprint()

    testo = str(sprint)

    assert "Sprint 'Sprint 1'" in testo
    assert "ATTIVO" in testo
    assert "Obiettivo: Rilasciare login" in testo


def test_str_sprint_con_ticket():
    sprint = Sprint(
        "Sprint 1",
        "Rilasciare login",
    )

    ticket = FeatureTicket(
        "FEA-1",
        "Login SSO",
        story_points=5,
    )

    sprint.aggiungi_ticket(ticket)

    testo = str(sprint)

    assert "Ticket inclusi: 1" in testo


# ------------------------------ ESECUZIONE DIRETTA DEL FILE ------------------------------
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