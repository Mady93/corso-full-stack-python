import math


def somma(a: float, b: float) -> float:
    """Return the sum of a and b."""
    return a + b


def sottrai(a: float, b: float) -> float:
    """Return the difference between a and b."""
    return a - b


def moltiplica(a: float, b: float) -> float:
    """Return the product of a and b."""
    return a * b


def dividi(a: float, b: float) -> float:
    """Return the quotient of a divided by b.

    Raises ZeroDivisionError if b is zero.
    """
    # Controllo che il divisore non sia zero.
    if b == 0:
        raise ZeroDivisionError("division by zero is not allowed")

    # Eseguo la divisione.
    return a / b


def potenza(a: float, b: float) -> float:
    """Return a raised to the power of b.

    Raises ValueError if a is negative and b is not an integer.
    """
    # Controllo che una base negativa non abbia un esponente non intero.
    if a < 0 and b != int(b):
        raise ValueError("negative base with non-integer exponent")

    # Eseguo la potenza.
    return a ** b


def resto(a: float, b: float) -> float:
    """Return the remainder of a divided by b.

    Raises ZeroDivisionError if b is zero.
    """
    # Controllo che il divisore non sia zero.
    if b == 0:
        raise ZeroDivisionError("remainder with zero divisor is not allowed")

    # Calcolo il resto della divisione.
    return a % b


def radice_quadrata(a: float) -> float:
    """Return the square root of a.

    Raises ValueError if a is negative.
    """
    # Controllo che il numero non sia negativo.
    if a < 0:
        raise ValueError("square root of a negative number")

    # Calcolo la radice quadrata.
    return math.sqrt(a)