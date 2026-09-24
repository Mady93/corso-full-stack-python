"""Shared, reusable validation helpers.
 
No try/except here: every function prints a clear error message and
returns True or False. The caller just checks the result with a plain
`if` -- that's enough to build a robust, "web app style" system without
needing exceptions.
"""
 
 
def testo_valido(valore, nome_campo: str) -> bool:
    """Return True if valore is a non-empty string."""
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


def intero_positivo(valore, nome_campo: str) -> bool:
    """Return True if valore is an int (not a bool) and strictly > 0."""
    # isinstance(valore, bool) viene controllato separatamente perché in Python
    # bool è una sottoclasse di int: isinstance(True, int) restituisce True.
    # Senza questo controllo, True/False verrebbero accettati erroneamente
    # come numeri validi.
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


def intero_non_negativo(valore, nome_campo: str) -> bool:
    """Return True if valore is an int (not a bool) and >= 0."""
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