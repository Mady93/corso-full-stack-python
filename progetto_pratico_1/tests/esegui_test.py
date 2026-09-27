"""
Lancia in sequenza tutte le funzioni test_* definite nei file test_ticket.py,
test_utente.py, test_sprint.py, test_gestionale.py, senza usare unittest:
importa ogni modulo ed esegue tutto cio' che inizia per "test_".

Uso: python3 tests/esegui_test.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))

import test_gestionale
import test_sprint
import test_ticket
import test_utente
import test_configurazione_team

MODULI_TEST = [test_ticket, test_utente, test_sprint, test_gestionale, test_configurazione_team]


def esegui_tutti() -> None:
    totale = 0
    falliti = 0
    for modulo in MODULI_TEST:
        for nome in dir(modulo):
            if nome.startswith("test_"):
                funzione = getattr(modulo, nome)
                totale += 1
                try:
                    funzione()
                    print(f"[OK]   {modulo.__name__}.{nome}")
                except AssertionError as e:
                    falliti += 1
                    print(f"[FAIL] {modulo.__name__}.{nome}: {e}")
                except Exception as e:
                    falliti += 1
                    print(f"[ERRORE] {modulo.__name__}.{nome}: {e}")

    print(f"\nTotale test: {totale} | Superati: {totale - falliti} | Falliti: {falliti}")


if __name__ == "__main__":
    esegui_tutti()