# Attività»» 2 — Script principale calcolatrice Guidata
# Consegna

# Crea main_calcolatrice.py. Il programma deve:

#     Importare il modulo calcolatrice.
#     Chiedere due numeri con float(input(...)).
#     Chiedere un'operazione: +, -, *, /.
#     Usare if/elif/else per chiamare la funzione corretta.
#     Stampare il risultato.

"""Script principale della calcolatrice.

Chiede all'utente due numeri e un'operazione (+, -, *, /), chiama la
funzione corrispondente del modulo calcolatrice e stampa il risultato.
"""

import calcolatrice


# Mostro le operazioni disponibili e chiedo il numero corrispondente
print("1. Somma")
print("2. Sottrazione")
print("3. Moltiplicazione")
print("4. Divisione")
print("5. Potenza")
print("6. Resto")
print("7. Radice quadrata")


# Controllo l'operazione e continuo a chiederla finché non viene inserita correttamente
while True:
    try:
        operazione = int(input("Scegli l'operazione: "))

        if operazione >= 1 and operazione <= 7:
            break

        print("Operazione non valida.")

    except ValueError:
        print("Inserisci un numero da 1 a 7.")


# La radice quadrata usa solo il primo numero
if operazione == 7:

    # Controllo il primo numero e continuo a chiederlo finché non viene inserito un numero
    while True:
        try:
            a = float(input("Inserisci il numero: "))
            break
        except ValueError:
            print("Inserisci un numero valido.")

    # Controllo che il numero sia positivo prima della radice
    while a < 0:
        print("Errore: non si può calcolare la radice di un numero negativo")

        while True:
            try:
                a = float(input("Inserisci il primo numero: "))
                break
            except ValueError:
                print("Inserisci un numero valido.")

    risultato = calcolatrice.radice_quadrata(a)
    print(f"Risultato: {risultato}")


else:

    # Controllo il primo numero e continuo a chiederlo finché non viene inserito un numero
    while True:
        try:
            a = float(input("Inserisci il primo numero: "))
            break
        except ValueError:
            print("Inserisci un numero valido.")


    # Controllo il secondo numero e continuo a chiederlo finché non viene inserito un numero
    while True:
        try:
            b = float(input("Inserisci il secondo numero: "))
            break
        except ValueError:
            print("Inserisci un numero valido.")


    # Controllo l'operazione e chiamo la funzione corrispondente
    if operazione == 1:
        risultato = calcolatrice.somma(a, b)
        print(f"Risultato: {risultato}")

    elif operazione == 2:
        risultato = calcolatrice.sottrai(a, b)
        print(f"Risultato: {risultato}")

    elif operazione == 3:
        risultato = calcolatrice.moltiplica(a, b)
        print(f"Risultato: {risultato}")

    elif operazione == 4:
        # Controllo il divisore prima di eseguire la divisione
        while b == 0:
            print("Errore: non si può dividere per zero")

            while True:
                try:
                    b = float(input("Inserisci il secondo numero: "))
                    break
                except ValueError:
                    print("Inserisci un numero valido.")

        risultato = calcolatrice.dividi(a, b)
        print(f"Risultato: {risultato}")

    # Attività»» 6 — Estensione calcolatrice Sfida
    # Consegna

    # Estendi calcolatrice.py con:
    # potenza(a, b)
    # resto(a, b)
    # radice_quadrata(a)

    # Aggiungi le stesse funzioni in main_calcolatrice.py con nuove operazioni: **, %, sqrt.

    # Gestisci gli errori:

    #     Divisione per zero.
    #     Radice di numero negativo.

    elif operazione == 5:
        risultato = calcolatrice.potenza(a, b)
        print(f"Risultato: {risultato}")

    elif operazione == 6:
        # Controllo il divisore prima di calcolare il resto
        while b == 0:
            print("Errore: non si può calcolare il resto con zero")

            while True:
                try:
                    b = float(input("Inserisci il secondo numero: "))
                    break
                except ValueError:
                    print("Inserisci un numero valido.")

        risultato = calcolatrice.resto(a, b)
        print(f"Risultato: {risultato}")