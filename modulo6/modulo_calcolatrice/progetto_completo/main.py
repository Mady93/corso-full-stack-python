# Consegna

# Crea una cartella progetto_completo con:

#     calcolatrice.py (con tutte le funzioni).
#     utility_casuali.py.
#     main.py che permette di scegliere tra:
#         Calcolatrice.
#         Gioco del numero casuale.
#         Lancio dado / estrazione nome.

# main.py deve importare i moduli e delegare le operazioni.

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
    """Chiede operazione e numeri, poi delega il calcolo al modulo calcolatrice."""

    # Mostro le operazioni disponibili e chiedo il numero corrispondente
    print("1. Somma")
    print("2. Sottrazione")
    print("3. Moltiplicazione")
    print("4. Divisione")
    print("5. Potenza")
    print("6. Resto")
    print("7. Radice quadrata")

    # Continuo a chiedere l'operazione finché non viene inserita correttamente
    while True:
        try:
            operazione = int(input("Scegli l'operazione: "))

            if operazione >= 1 and operazione <= 7:
                break

            print("Operazione non valida.")

        except ValueError:
            print("Inserisci un numero da 1 a 7.")

    # Continuo a chiedere il primo numero finché non viene inserito un numero
    while True:
        try:
            a = float(input("Primo numero: "))
            break
        except ValueError:
            print("Inserisci un numero.")

    if operazione == 7:
        while True:
            try:
                risultato = calcolatrice.radice_quadrata(a)
                print(f"Risultato: {risultato}")
                break
            except ValueError:
                print("Non puoi calcolare la radice di un numero negativo.")
                while True:
                    try:
                        a = float(input("Inserisci un numero positivo: "))
                        break
                    except ValueError:
                        print("Inserisci un numero.")

    else:
        # Continuo a chiedere il secondo numero finché non viene inserito correttamente
        while True:
            try:
                b = float(input("Secondo numero: "))

                # Controllo divisione e resto per evitare il divisore zero
                if (operazione == 4 or operazione == 6) and b == 0:
                    print("Il divisore non può essere zero.")
                    continue

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

                print(f"Risultato: {risultato}")
                break

            except ValueError:
                print("Inserisci un numero.")
            except ZeroDivisionError:
                print("Il divisore non può essere zero.")


def gioco_numero() -> None:
    """Gioco: indovina il numero pensato dal computer tra 1 e 100."""

    segreto = random.randint(1, 100)
    tentativi = 0

    print("Ho pensato un numero tra 1 e 100.")

    while True:
        try:
            tentativo = int(input("Tuo tentativo: "))

            # Controllo che il numero sia compreso tra 1 e 100
            if tentativo < 1 or tentativo > 100:
                print("Inserisci un numero tra 1 e 100.")
                continue

        except ValueError:
            print("Inserisci un numero intero.")
            continue

        tentativi += 1

        if tentativo < segreto:
            print("Troppo basso!")
        elif tentativo > segreto:
            print("Troppo alto!")
        else:
            print(f"Hai indovinato in {tentativi} tentativi!")
            break


def menu_casuali() -> None:
    """Lancio del dado, estrazione di un nome o password, tramite utility_casuali."""

    # Mostro le operazioni disponibili e chiedo il numero corrispondente
    print("1. Lancia il dado")
    print("2. Estrai un nome")
    print("3. Genera una password")

    # Continuo a chiedere la scelta finché non viene inserita correttamente
    while True:
        try:
            scelta = int(input("Scegli cosa vuoi fare: "))

            if scelta == 1:
                print(f"Hai ottenuto: {utility_casuali.lancia_dado()}")
                break

            elif scelta == 2:
                nomi = ["Anna", "Luca", "Giulia", "Marco", "Sara"]
                print(f"Nome estratto: {utility_casuali.estrai_nome(nomi)}")
                break

            elif scelta == 3:
                # Continuo a chiedere la lunghezza finché non viene inserito un numero
                while True:
                    try:
                        lunghezza = int(input("Lunghezza della password: "))

                        if lunghezza > 0:
                            break

                        print("La lunghezza deve essere maggiore di zero.")

                    except ValueError:
                        print("Inserisci un numero intero.")

                print(f"Password: {utility_casuali.genera_password(lunghezza)}")
                break

            else:
                print("Scelta non valida.")

        except ValueError:
            print("Inserisci un numero da 1 a 3.")


def main() -> None:
    """Mostra il menu principale e delega alle funzioni giuste."""

    while True:
        print("\n=== MENU ===")
        print("1. Calcolatrice")
        print("2. Gioco del numero casuale")
        print("3. Dado / estrazione nome / password")
        print("0. Esci")

        scelta = input("Scelta: ").strip()

        if scelta == "1":
            menu_calcolatrice()

        elif scelta == "2":
            gioco_numero()

        elif scelta == "3":
            menu_casuali()

        elif scelta == "0":
            print("Arrivederci!")
            break

        else:
            print("Scelta non valida. Inserisci 1, 2, 3 oppure 0")


if __name__ == "__main__":
    main()