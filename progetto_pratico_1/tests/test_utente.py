"""
Test manuali sul modulo Utente.

Verifica:
- validazione dei dati in ingresso
- ruoli
- permessi
- proprieta'
- limite di carico dello sviluppatore
- modifica del limite
- incremento/decremento del carico
- rappresentazione testuale
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from eccezioni.eccezioni_custom import ValidazioneError, RuoloNonValidoError
from modelli.utente import Utente


# ----------------------- COSTRUZIONE E VALIDAZIONE -----------------------
def test_creazione_utente_dev():
    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
        ["VIEW_TICKET", "COMMENT_TICKET"],
        max_ticket=2,
        dipartimento="Core",
    )

    assert dev.username == "mrossi"
    assert dev.email == "m@test.it"
    assert dev.ruolo == "DEV"
    assert dev.max_ticket == 2
    assert dev.ticket_in_carico == 0
    assert dev.dipartimento == "Core"


def test_creazione_utente_pm():
    pm = Utente(
        "lbianchi",
        "l@test.it",
        "PM",
        ["VIEW_TICKET", "CREATE_TICKET"],
        dipartimento="Core",
    )

    assert pm.username == "lbianchi"
    assert pm.email == "l@test.it"
    assert pm.ruolo == "PM"
    assert pm.max_ticket == 0
    assert pm.ticket_in_carico == 0
    assert pm.dipartimento == "Core"


def test_username_vuoto():
    try:
        Utente("", "m@test.it", "DEV")
        assert False
    except ValidazioneError:
        pass


def test_username_solo_spazi():
    try:
        Utente("   ", "m@test.it", "DEV")
        assert False
    except ValidazioneError:
        pass


def test_email_vuota():
    try:
        Utente("mrossi", "", "DEV")
        assert False
    except ValidazioneError:
        pass


def test_email_solo_spazi():
    try:
        Utente("mrossi", "   ", "DEV")
        assert False
    except ValidazioneError:
        pass


def test_ruolo_non_valido():
    try:
        Utente("mrossi", "m@test.it", "ADMIN")
        assert False
    except RuoloNonValidoError:
        pass


def test_ruolo_maiuscolo_automaticamente():
    dev = Utente("mrossi", "m@test.it", "dev")

    assert dev.get_ruolo() == "DEV"
    assert dev.ruolo == "DEV"


def test_max_ticket_negativo():
    try:
        Utente(
            "mrossi",
            "m@test.it",
            "DEV",
            max_ticket=-1,
        )
        assert False
    except ValidazioneError:
        pass


# ----------------------- RUOLI E PERMESSI -----------------------
def test_utente_dev_ruolo():
    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
        [
            "VIEW_TICKET",
            "COMMENT_TICKET",
            "CHANGE_STATUS",
        ],
        max_ticket=2,
    )

    assert dev.get_ruolo() == "DEV"


def test_utente_pm_ruolo():
    pm = Utente(
        "lbianchi",
        "l@test.it",
        "PM",
        [
            "VIEW_TICKET",
            "COMMENT_TICKET",
            "CREATE_TICKET",
            "ASSIGN_TICKET",
            "CREATE_SPRINT",
            "MANAGE_SPRINT",
        ],
        dipartimento="Core",
    )

    assert pm.get_ruolo() == "PM"


def test_permessi_dev():
    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
        [
            "VIEW_TICKET",
            "COMMENT_TICKET",
            "CHANGE_STATUS",
        ],
        max_ticket=2,
    )

    assert dev.ha_permesso("VIEW_TICKET")
    assert dev.ha_permesso("COMMENT_TICKET")
    assert dev.ha_permesso("CHANGE_STATUS")

    assert not dev.ha_permesso("CREATE_TICKET")
    assert not dev.ha_permesso("ASSIGN_TICKET")


def test_permessi_pm():
    pm = Utente(
        "lbianchi",
        "l@test.it",
        "PM",
        [
            "VIEW_TICKET",
            "COMMENT_TICKET",
            "CREATE_TICKET",
            "ASSIGN_TICKET",
            "CREATE_SPRINT",
            "MANAGE_SPRINT",
        ],
        dipartimento="Core",
    )

    assert pm.ha_permesso("CREATE_TICKET")
    assert pm.ha_permesso("ASSIGN_TICKET")
    assert pm.ha_permesso("CREATE_SPRINT")
    assert pm.ha_permesso("MANAGE_SPRINT")

    assert not pm.ha_permesso("CHANGE_STATUS")


def test_get_permessi():
    permessi = [
        "VIEW_TICKET",
        "COMMENT_TICKET",
        "CHANGE_STATUS",
    ]

    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
        permessi,
        max_ticket=2,
    )

    assert dev.get_permessi() == permessi


def test_get_permessi_restituisce_copia():
    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
        ["VIEW_TICKET"],
        max_ticket=2,
    )

    permessi = dev.get_permessi()
    permessi.append("CREATE_TICKET")

    assert dev.get_permessi() == ["VIEW_TICKET"]


def test_utente_senza_permessi():
    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
        max_ticket=2,
    )

    assert dev.get_permessi() == []
    assert not dev.ha_permesso("VIEW_TICKET")


# ----------------------- LIMITE TICKET E CARICO -----------------------
def test_puo_accettare_ticket_entro_il_limite():
    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
        [],
        max_ticket=2,
    )

    assert dev.puo_accettare_ticket()

    dev.incrementa_ticket()
    assert dev.puo_accettare_ticket()

    dev.incrementa_ticket()
    assert not dev.puo_accettare_ticket()


def test_incrementa_ticket():
    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
        [],
        max_ticket=3,
    )

    assert dev.ticket_in_carico == 0

    dev.incrementa_ticket()
    assert dev.ticket_in_carico == 1

    dev.incrementa_ticket()
    assert dev.ticket_in_carico == 2


def test_decrementa_ticket():
    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
        [],
        max_ticket=3,
    )

    dev.incrementa_ticket()
    dev.incrementa_ticket()

    assert dev.ticket_in_carico == 2

    dev.decrementa_ticket()

    assert dev.ticket_in_carico == 1


def test_decrementa_ticket_non_scende_sotto_zero():
    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
        [],
        max_ticket=2,
    )

    dev.decrementa_ticket()
    dev.decrementa_ticket()

    assert dev.ticket_in_carico == 0


def test_impostare_limite_ticket():
    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
        [],
        max_ticket=2,
    )

    assert dev.max_ticket == 2

    dev.impostare_limite_ticket(5)

    assert dev.max_ticket == 5


def test_impostare_limite_ticket_negativo():
    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
        [],
        max_ticket=2,
    )

    try:
        dev.impostare_limite_ticket(-1)
        assert False
    except ValidazioneError:
        pass

    assert dev.max_ticket == 2


def test_limite_zero():
    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
        [],
        max_ticket=0,
    )

    assert not dev.puo_accettare_ticket()


# ----------------------- RAPPRESENTAZIONE TESTUALE -----------------------
def test_str_dev():
    dev = Utente(
        "mrossi",
        "m@test.it",
        "DEV",
        [],
        max_ticket=2,
    )

    testo = str(dev)

    assert "[DEV]" in testo
    assert "Username: mrossi" in testo
    assert "Email: m@test.it" in testo
    assert "Carico: 0/2" in testo


def test_str_pm():
    pm = Utente(
        "lbianchi",
        "l@test.it",
        "PM",
        [],
        dipartimento="Core",
    )

    testo = str(pm)

    assert "[PM]" in testo
    assert "Username: lbianchi" in testo
    assert "Email: l@test.it" in testo
    assert "Dipartimento: Core" in testo
    assert "Carico:" not in testo


# ----------------------- ESECUZIONE DIRETTA DEL FILE -----------------------
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