import random

import calcolatrice
import utility_casuali


OPERAZIONI_DUE_NUMERI = {
    "+": calcolatrice.somma,
    "-": calcolatrice.sottrai,
    "*": calcolatrice.moltiplica,
    "/": calcolatrice.dividi,
    "**": calcolatrice.potenza,
    "%": calcolatrice.resto,
}


def menu_calcolatrice() -> None:
    """Ask for an operation and numbers, then delegate the calculation."""

    # Mostro le operazioni disponibili.
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Power")
    print("6. Remainder")
    print("7. Square root")

    # Continuo a chiedere l'operazione finché non viene inserita correttamente.
    while True:
        try:
            operazione = int(input("Choose the operation: "))

            if 1 <= operazione <= 7:
                break

            print("Invalid operation.")

        except ValueError:
            print("Enter a number from 1 to 7.")

    # Chiedo il primo numero e controllo la conversione.
    while True:
        try:
            a = float(input("First number: "))

        except ValueError:
            print("Enter a valid number.")

        else:
            break

    # La radice quadrata richiede solamente il primo numero.
    if operazione == 7:

        # Provo a calcolare la radice quadrata e gestisco un valore negativo.
        while True:
            try:
                risultato = calcolatrice.radice_quadrata(a)

            except ValueError:
                print("You cannot calculate the square root of a negative number.")

                # Richiedo un nuovo numero dopo l'errore.
                while True:
                    try:
                        a = float(input("Enter a non-negative number: "))

                    except ValueError:
                        print("Enter a valid number.")

                    else:
                        break

            else:
                print(f"Result: {risultato}")
                break

            finally:
                print("Square root calculation attempt completed.")

    else:
        # Chiedo il secondo numero e controllo la conversione.
        while True:
            try:
                b = float(input("Second number: "))

                # Controllo divisione e resto per evitare il divisore zero.
                if (operazione == 4 or operazione == 6) and b == 0:
                    raise ZeroDivisionError("zero divisor")

                # Scelgo la funzione da eseguire in base all'operazione.
                if operazione == 1:
                    risultato = calcolatrice.somma(a, b)

                elif operazione == 2:
                    risultato = calcolatrice.sottrai(a, b)

                elif operazione == 3:
                    risultato = calcolatrice.moltiplica(a, b)

                elif operazione == 4:
                    risultato = calcolatrice.dividi(a, b)

                elif operazione == 5:
                    risultato = calcolatrice.potenza(a, b)

                elif operazione == 6:
                    risultato = calcolatrice.resto(a, b)

            except ValueError:
                print("Enter a valid number.")

            except ZeroDivisionError:
                print("The divisor cannot be zero.")

            else:
                print(f"Result: {risultato}")
                break

            finally:
                print("Calculation attempt completed.")


def gioco_numero() -> None:
    """Play a game in which the user guesses a random number from 1 to 100."""

    # Genero il numero segreto.
    segreto = random.randint(1, 100)
    tentativi = 0

    print("I have chosen a number between 1 and 100.")

    # Continuo a chiedere tentativi finché l'utente non indovina.
    while True:
        try:
            tentativo = int(input("Your guess: "))

            # Controllo che il numero sia compreso tra 1 e 100.
            if tentativo < 1 or tentativo > 100:
                raise ValueError("number outside the allowed range")

        except ValueError:
            print("Enter an integer between 1 and 100.")
            continue

        else:
            tentativi += 1

            if tentativo < segreto:
                print("Too low!")

            elif tentativo > segreto:
                print("Too high!")

            else:
                print(f"You guessed it in {tentativi} attempts!")
                break

        finally:
            print("Guess attempt completed.")


def menu_casuali() -> None:
    """Handle dice, name extraction, and password generation."""

    # Mostro le operazioni disponibili.
    print("1. Roll the dice")
    print("2. Pick a name")
    print("3. Generate a password")

    # Continuo a chiedere la scelta finché non viene inserita correttamente.
    while True:
        try:
            scelta = int(input("Choose what you want to do: "))

            if scelta == 1:
                print(f"Result: {utility_casuali.lancia_dado()}")

            elif scelta == 2:
                nomi = ["Anna", "Luca", "Giulia", "Marco", "Sara"]
                print(
                    f"Selected name: "
                    f"{utility_casuali.estrai_nome(nomi)}"
                )

            elif scelta == 3:

                # Continuo a chiedere la lunghezza finché non è valida.
                while True:
                    try:
                        lunghezza = int(input("Password length: "))

                        if lunghezza <= 0:
                            raise ValueError("length must be positive")

                    except ValueError:
                        print("Enter a positive integer.")

                    else:
                        print(
                            f"Password: "
                            f"{utility_casuali.genera_password(lunghezza)}"
                        )
                        break

                    finally:
                        print("Password length check completed.")

            else:
                print("Invalid choice.")

            if scelta in (1, 2, 3):
                break

        except ValueError:
            print("Enter a number from 1 to 3.")

        else:
            print("Operation completed.")

        finally:
            print("Menu operation attempt completed.")


def main() -> None:
    """Display the main menu and delegate each option to the proper function."""

    # Mostro il menu principale.
    while True:
        print("\n=== MENU ===")
        print("1. Calculator")
        print("2. Random number game")
        print("3. Dice / name extraction / password")
        print("0. Exit")

        scelta = input("Choice: ").strip()

        if scelta == "1":
            menu_calcolatrice()

        elif scelta == "2":
            gioco_numero()

        elif scelta == "3":
            menu_casuali()

        elif scelta == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Enter 1, 2, 3, or 0.")


if __name__ == "__main__":
    main()