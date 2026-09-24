"""Shared, reusable validation helpers"""

# Nessun try/except/raise: ogni funzione stampa un messaggio di errore chiaro
# e restituisce True o False. Il chiamante controlla semplicemente il risultato
# con un normale `if` -- sufficiente per costruire un sistema robusto, in stile
# "web app", senza utilizzare eccezioni.


def testo_valido(valore: object, nome_campo: str) -> bool:
    """Return True if valore is a non-empty string"""
    if not isinstance(valore, str):
        print(
            f"[Error] {nome_campo} must be a string, "
            f"received {type(valore).__name__}"
        )
        return False

    if not valore.strip():
        print(f"[Error] {nome_campo} cannot be empty")
        return False

    return True


def intero_positivo(valore: object, nome_campo: str) -> bool:
    """Return True if valore is an integer, not a boolean, and greater than zero"""
    # isinstance(valore, bool) è controllato a parte perché in Python
    # bool è sottoclasse di int: isinstance(True, int) è True. Senza
    # questo controllo, True/False passerebbero come numeri validi.
    if not isinstance(valore, int) or isinstance(valore, bool):
        print(
            f"[Error] {nome_campo} must be an integer, "
            f"received {type(valore).__name__}"
        )
        return False

    if valore <= 0:
        print(f"[Error] {nome_campo} must be a positive number (> 0)")
        return False

    return True


def intero_non_negativo(valore: object, nome_campo: str) -> bool:
    """Return True if valore is an integer, not a boolean, and greater than or equal to zero"""
    if not isinstance(valore, int) or isinstance(valore, bool):
        print(
            f"[Error] {nome_campo} must be an integer, "
            f"received {type(valore).__name__}"
        )
        return False

    if valore < 0:
        print(f"[Error] {nome_campo} cannot be negative")
        return False

    return True


def numero_positivo(valore: object, nome_campo: str) -> bool:
    """Return True if valore is a positive integer or float, not a boolean"""
    if not isinstance(valore, (int, float)) or isinstance(valore, bool):
        print(
            f"[Error] {nome_campo} must be a number, "
            f"received {type(valore).__name__}"
        )
        return False

    if valore <= 0:
        print(f"[Error] {nome_campo} must be a positive number (> 0)")
        return False

    return True


def booleano_valido(valore: object, nome_campo: str) -> bool:
    """Return True if valore is exactly True or False"""
    if not isinstance(valore, bool):
        print(
            f"[Error] {nome_campo} must be a boolean (True/False), "
            f"received {type(valore).__name__}"
        )
        return False

    return True