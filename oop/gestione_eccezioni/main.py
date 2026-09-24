# Mini progetto: conto bancario sicuro
# Consegna

# Realizza una classe Conto con:

#     Intestatario e saldo.
#     Metodo deposita().
#     Metodo preleva().
#     Eccezione personalizzata per saldo insufficiente.
#     Controllo dei valori negativi con un'eccezione appropriata.

# Comportamenti da gestire

#     Deposito positivo.
#     Prelievo disponibile.
#     Prelievo superiore al saldo.
#     Importo negativo.
#     Messaggio finale sempre visualizzato.

# Usa try, except, else, finally, raise e almeno una classe di eccezione personalizzata.

import sys

from conto_bancario.conto import Conto
from exceptions.app_exception import (
    AppException,
    ValidationError,
)
from handler import gestisci_eccezione
from handler_success import gestisci_successo


def leggi_float(prompt: str, messaggio_errore: str) -> float:
    """Legge un numero decimale da input o lancia una ValidationError con messaggio personalizzato"""
    try:
        return float(input(prompt))
    except ValueError as e:
        raise ValidationError(messaggio_errore) from e


def main() -> None:
    """Run the bank account application"""

    sys.excepthook = gestisci_eccezione

    conto = Conto("Mario Rossi", 100.0)

    while True:
        print()
        print("-------------- BANK ACCOUNT --------------")
        print(f"Account holder: {conto.intestatario}")
        print(f"Balance: {conto.saldo:.2f} €")
        print()
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Show balance")
        print("0. Exit")

        interruzione = False

        try:
            # Per la scelta del menu
            scelta = int(
                leggi_float("Choose an option: ", "Please enter a valid menu option number")
            )

            match scelta:
                case 1:
                    # Messaggio personalizzato per il deposito
                    importo = leggi_float(
                        "Deposit amount: ",
                        "The deposit amount must be a valid number (e.g. 10.50)"
                    )

                    conto.deposita(importo)

                    gestisci_successo(
                        message="Deposit completed successfully",
                    )

                case 2:
                    # Messaggio personalizzato per il prelievo
                    importo = leggi_float(
                        "Withdrawal amount: ",
                        "The withdrawal amount must be a valid number (e.g. 10.50)"
                    )

                    conto.preleva(importo)

                    gestisci_successo(
                        message="Withdrawal completed successfully",
                    )

                case 3:
                    gestisci_successo(
                        data={
                            "intestatario": conto.intestatario,
                            "saldo": conto.saldo,
                        },
                        message="Balance retrieved successfully",
                    )

                case 0:
                    gestisci_successo(
                        message="Goodbye!",
                    )
                    break

                case _:
                    raise ValidationError(
                        "Invalid menu option"
                    )

        except KeyboardInterrupt:
            interruzione = True
            print("\nGoodbye!")
            break

        except AppException as errore:
            # Tutte le eccezioni (sia da leggi_float che da Conto) arrivano qui!
            gestisci_eccezione(
                type(errore),
                errore,
                errore.__traceback__,
            )

        finally:
            if not interruzione:
                print("Operation finished")


if __name__ == "__main__":
    main()