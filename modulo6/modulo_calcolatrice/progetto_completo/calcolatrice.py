import math

def somma(a: float, b: float) -> float:
    """Restituisce la somma di a e b."""
    return a + b
 
 
def sottrai(a: float, b: float) -> float:
    """Restituisce la differenza tra a e b (a - b)."""
    return a - b
 
 
def moltiplica(a: float, b: float) -> float:
    """Restituisce il prodotto di a e b."""
    return a * b
 
 
def dividi(a: float, b: float) -> float:
    """Restituisce il quoziente di a diviso b.
    
    Solleva ZeroDivisionError se b è uguale a zero.
    """
    # Se il divisore è 0 sollevo io l'errore, con un messaggio chiaro
    if b == 0:
        raise ZeroDivisionError("divisione per zero non consentita")
    # Altrimenti posso dividere senza problemi
    return a / b


def potenza(a: float, b: float) -> float:
    """Restituisce a elevato alla b.

    Solleva ValueError se a è negativo e b non è un numero intero
    (il risultato non sarebbe un numero reale).
    """
    # Base negativa con esponente non intero (es. (-8) ** 0.5): risultato non reale
    if a < 0 and b != int(b):
        raise ValueError("base negativa con esponente non intero")
    # L'operatore ** eleva a alla potenza b
    return a ** b


def resto(a: float, b: float) -> float:
    """Restituisce il resto della divisione di a per b.

    Solleva ZeroDivisionError se b è uguale a zero.
    """
    # Anche per il resto, il divisore non può essere zero
    if b == 0:
        raise ZeroDivisionError("resto con divisore zero non consentito")
    # L'operatore % restituisce il resto della divisione
    return a % b


def radice_quadrata(a: float) -> float:
    """Restituisce la radice quadrata di a.

    Solleva ValueError se a è negativo.
    """
    # Non esiste la radice quadrata reale di un numero negativo
    if a < 0:
        raise ValueError("radice quadrata di un numero negativo")
    # math.sqrt calcola la radice quadrata
    return math.sqrt(a)