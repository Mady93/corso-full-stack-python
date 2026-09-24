# def is_prime(n, d=2):
#     # Caso base: numeri minori o uguali a 1 non sono primi
#     if n <= 1:
#         return False
#     # Se il divisore supera n - 1, è primo
#     if d * d > n:
#         return True
#     # Se è divisibile, non è primo
#     if n % d == 0:
#         return False
#     # Chiamata ricorsiva incrementando il divisore
#     return is_prime(n, d + 1)

# # Esempi di utilizzo
# print(is_prime(11))  # Restituisce True (è primo)
# print(is_prime(4))   # Restituisce False (non è primo) 

def esercizio_conversione():
    """
    Mini esercizio: funzione di conversione

    Definisci una funzione chiamata celsius_a_fahrenheit che riceve
    una temperatura Celsius e restituisce Fahrenheit.
    """

    def celsius_a_fahrenheit(celsius: float) -> float:
        return celsius * 9 / 5 + 32

    def chiedi_celsius() -> float:
        while True:
            try:
                return float(
                    input("Inserisci la temperatura in Celsius: ")
                )
            except ValueError:
                print("Errore: devi inserire un numero")

    celsius = chiedi_celsius()

    print(
        f"{celsius} Celsius equivalgono "
        f"a {celsius_a_fahrenheit(celsius)} Fahrenheit"
    )



def stampa_profilo(nome, *interessi, **dati) -> None:
    
    # Stampa profilo
    print("\n" + "-" * 60)
    print(f"Nome: {nome}")

    print("\nInteressi:")
    print("-" * 60)

    for interesse in interessi:
        print(f"- {interesse}")

    print("\nDati aggiuntivi:")
    print("-" * 60)

    for chiave, valore in dati.items():
        print(f"{chiave}: {valore}")


def esercizio_profilo():
    """
    Mini esercizio: profilo flessibile
    
    Definisci una funzione stampa_profilo che riceve:
    
    Un parametro obbligatorio nome.
    Un numero variabile di interessi con *interessi.
    Informazioni aggiuntive con **dati.
    """

    # Input e controllo nome
    while True:

        nome = input("Inserisci il nome: ").strip()

        if not nome:
            print("Errore: il nome non può essere vuoto")
            continue

        if not nome.replace(" ", "").isalpha():
            print("Errore: devi inserire un nome valido")
            continue

        break

    # Input e controllo interessi
    while True:

        interessi_input = input(
            "Inserisci gli interessi separati da virgola: "
        )

        if not interessi_input.strip():
            print("Errore: devi inserire almeno un interesse")
            continue

        interessi = [
            interesse.strip()
            for interesse in interessi_input.split(",")
        ]

        if any(not interesse for interesse in interessi):
            print("Errore: non puoi lasciare interessi vuoti")
            continue

        break

    # Input dati aggiuntivi
    dati = {}

    while True:

        chiave = input(
            "Inserisci il nome del dato aggiuntivo "
            "(Invio per terminare): "
        ).strip()

        if not chiave:
            break

        valore = input(
            f"Inserisci il valore di '{chiave}': "
        ).strip()

        if not valore:
            print("Errore: il valore non può essere vuoto")
            continue

        dati[chiave] = valore

    # Controllo dati aggiuntivi
    if not dati:
        print("Errore: devi inserire almeno un dato aggiuntivo")
        return

    # Chiamata della funzione
    stampa_profilo(nome, *interessi, **dati)



# Mini esercizio: funzione documentata
#     Consegna

#     Crea documentata.py.

#     Definisci una funzione calcola_consumo che:

#     Riceve chilometri e litri come float.
#     Restituisce il consumo in km/l come float.
#     Contiene una docstring con descrizione, Args e Returns.
#     Usa type hint su parametri e ritorno.

#     consumo = chilometri / litri

#     Prova ad aggiungere print(calcola_consumo.__doc__) per vedere la docstring dal programma.
def calcola_consumo(km: float, litri: float) -> float:
    """
    Calcola il consumo di carburante in chilometri per litro.

    Args:
        km (float): Chilometri percorsi.
        litri (float): Litri di carburante consumati.

    Returns:
        float: Consumo in chilometri per litro.

    Raises:
        ValueError: Se i chilometri sono negativi o i litri sono
                    minori o uguali a zero.
    """

    if km < 0:
        # throw new IllegalArgumentException("I chilometri non possono essere negativi")
        raise ValueError("I chilometri non possono essere negativi")

    if litri <= 0:
        raise ValueError("I litri devono essere maggiori di zero")

    return km / litri


def esercizio_calcola_consumo() -> None:

    while True:
        try:
            km = float(input("Inserisci i chilometri percorsi: "))

            if km < 0:
                print("Errore: i chilometri non possono essere negativi")
                continue

            break

        except ValueError:
            print("Errore: devi inserire un numero")


    while True:
        try:
            litri = float(input("Inserisci i litri consumati: "))

            if litri <= 0:
                print("Errore: i litri devono essere maggiori di zero")
                continue

            break

        except ValueError:
            print("Errore: devi inserire un numero")


    try:
        consumo = calcola_consumo(km, litri)
        print(f"Consumo: {consumo:.2f} km/l")

        print("\n" + "-" * 60)
        print("DOCUMENTAZIONE DELLA FUNZIONE")
        print("-" * 60)
        print(calcola_consumo.__doc__)
        # help(calcola_consumo) 

    except ValueError as errore:
        print(f"Errore: {errore}")



# MENU

while True:

    print("\n" + "=" * 60)
    print("MENU ESERCIZI")
    print("=" * 60)

    print("1. Conversione Celsius → Fahrenheit")
    print("2. Profilo flessibile")
    print("3. Calcola consumo")
    print("0. Esci")

    scelta = input("Scegli un esercizio: ")

    match scelta:

        case "1":
            esercizio_conversione()

        case "2":
            esercizio_profilo()

        case "3":
            esercizio_calcola_consumo()

        case "0":
            print("Programma terminato")
            break

        case _:
            print("Errore: scelta non valida")