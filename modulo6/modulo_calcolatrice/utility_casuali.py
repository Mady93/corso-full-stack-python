# Attività»» 4 — Modulo utility casuali Autonoma
# Consegna

# Crea utility_casuali.py con:
# lancia_dado()
# estrai_nome(nomi)
# genera_password(lunghezza)

# Ogni funzione deve:

#     Avere docstring e type hint.
#     Usare random internamente.
#     Restituire un valore con return.

import random
import string
 
 
def lancia_dado() -> int:
    """Simula il lancio di un dado a sei facce e restituisce il risultato."""

    # randint() genera un numero casuale compreso tra 1 e 6
    return random.randint(1, 6)
 
 
def estrai_nome(nomi: list[str]) -> str:
    """Restituisce un nome scelto a caso dalla lista.
 
    Solleva ValueError se la lista è vuota.
    """

    # Controllo che la lista non sia vuota prima di estrarre un nome
    if not nomi:
        raise ValueError("la lista dei nomi è vuota")

    # choice() sceglie casualmente un elemento della lista
    return random.choice(nomi)
 
 
def genera_password(lunghezza: int) -> str:
    """Restituisce una password casuale di lettere, cifre e simboli."""

    # Unisco lettere, numeri e simboli in un'unica stringa di caratteri disponibili
    caratteri = string.ascii_letters + string.digits + string.punctuation

    # Scelgo casualmente un carattere per ogni posizione della password e li unisco in una stringa
    return "".join(random.choice(caratteri) for _ in range(lunghezza))
