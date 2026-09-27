"""
Gerarchia di eccezioni custom del dominio Mini-Jira.

Tutte le eccezioni di business ereditano da JiraException: questo permette
a main.py di distinguere, con un unico except, tra errori di regola di
business (gestiti, messaggio pulito per l'utente) ed errori di
programmazione realmente imprevisti (bug veri, da loggare come tali).
"""


class JiraException(Exception):
    """Eccezione base del sistema Mini-Jira."""
    pass


class ValidazioneError(JiraException):
    """Lanciata quando i dati inseriti da tastiera non superano i controlli."""
    pass


class TransizioneStatoNonValidaError(JiraException):
    """Lanciata quando si tenta un salto di stato vietato (es. TODO -> DONE)."""
    pass


class LimiteCaricoLavoroSuperatoError(JiraException):
    """Lanciata se uno sviluppatore ha gia' raggiunto il massimo dei ticket assegnabili."""
    pass


class ElementoNonTrovatoError(JiraException):
    """Lanciata quando un Ticket, Sprint o Utente cercato non esiste."""
    pass


class StatoSprintError(JiraException):
    """Lanciata per operazioni non ammesse sullo Sprint (doppio avvio, ticket duplicato, ecc.)."""
    pass


class DuplicatoError(JiraException):
    """Lanciata quando si registra un utente, ticket o sprint con una chiave gia' esistente.

    Prima veniva usato un generico ValueError: essendo un'eccezione builtin
    di Python e non un JiraException, finiva erroneamente nel ramo
    'ERRORE NON PREVISTO' del main invece che in quello di business.
    """
    pass


class RuoloNonValidoError(JiraException):
    """Lanciata quando un'operazione richiede un ruolo utente diverso da quello fornito
    (es. assegnare un ticket a un Project Manager invece che a uno Sviluppatore)."""
    pass


class TicketNonAssegnatoError(JiraException):
    """Lanciata quando si tenta di far avanzare un ticket che non ha ancora un assegnatario.

    Regola di business: non ha senso che un ticket lasci lo stato TODO se
    nessuno sviluppatore ne e' responsabile.
    """
    pass


class PermessoNegatoError(JiraException):
    """Lanciata quando un utente non ha il permesso richiesto."""
    pass

