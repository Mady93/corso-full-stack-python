"""
Helper per l'input da tastiera, con opzioni passate via *args e **kwargs 
per restare flessibili senza moltiplicare i
parametri posizionali.
"""

from eccezioni.eccezioni_custom import ValidazioneError


def leggi_stringa(prompt: str, min_len: int = 1, *args, **kwargs) -> str:
    """Legge una stringa da tastiera, verificando che non sia vuota (o
    piu' corta di min_len). kwargs['uppercase']=True forza il maiuscolo,
    utile per codici e opzioni di menu."""
    valore = input(prompt).strip()
    if len(valore) < min_len:
        raise ValidazioneError(f"L'input non puo' essere vuoto (almeno {min_len} caratteri)")

    if kwargs.get("uppercase", False):
        valore = valore.upper()

    return valore


def leggi_intero(prompt: str, min_val: int = None, max_val: int = None, *args, **kwargs) -> int:
    """Legge un valore numerico da tastiera, garantendo che sia un intero
    valido e, se richiesto, compreso in [min_val, max_val]."""
    testo = input(prompt).strip()
    try:
        valore = int(testo)
    except ValueError:
        raise ValidazioneError(f"'{testo}' non e' un numero intero valido.")

    if min_val is not None and valore < min_val:
        raise ValidazioneError(f"Il numero deve essere maggiore o uguale a {min_val}.")
    if max_val is not None and valore > max_val:
        raise ValidazioneError(f"Il numero non puo' superare {max_val}.")

    return valore


def valida_opzione_scelta(scelta: str, opzioni_valide: list, *args, **kwargs) -> str:
    """Controlla che l'input rientri in un insieme chiuso di opzioni consentite."""
    if scelta not in opzioni_valide:
        raise ValidazioneError(f"Scelta '{scelta}' non valida. Opzioni ammesse: {', '.join(opzioni_valide)}")
    return scelta