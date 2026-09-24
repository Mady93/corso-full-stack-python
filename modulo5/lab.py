# UTILITY
# -------------------------------------------------------------
def somma(a: float, b: float) -> float:
    """
    Somma due numeri.

    Args:
        a (float): Primo numero.
        b (float): Secondo numero.

    Returns:
        float: La somma dei due numeri.
    """
    return a + b


def sottrai(a: float, b: float) -> float:
    """
    Sottrae il secondo numero dal primo.

    Args:
        a (float): Primo numero.
        b (float): Secondo numero.

    Returns:
        float: La differenza tra i due numeri.
    """
    return a - b


def moltiplica(a: float, b: float) -> float:
    """
    Moltiplica due numeri.

    Args:
        a (float): Primo numero.
        b (float): Secondo numero.

    Returns:
        float: Il prodotto dei due numeri.
    """
    return a * b


def dividi(a: float, b: float) -> float:
    """
    Divide il primo numero per il secondo.

    Args:
        a (float): Dividendo.
        b (float): Divisore.

    Returns:
        float: Il risultato della divisione.
    """
    if b == 0:
        print("Divisione per zero non permessa")
        return 0
    else:
        return a / b


def potenza(a: float, b: float) -> float:
    """
    Eleva il primo numero alla potenza del secondo.

    Args:
        a (float): Base.
        b (float): Esponente.

    Returns:
        float: Il risultato della potenza.
    """
    return a ** b


def resto(a: float, b: float) -> float:
    """
    Calcola il resto della divisione tra due numeri.

    Args:
        a (float): Dividendo.
        b (float): Divisore.

    Returns:
        float: Il resto della divisione.
    """
    if b == 0:
        print("Il divisore non può essere zero")
        return 0
    else:
        return a % b


def inserisci_dati(
    con_operazione: bool = False
) -> tuple[float, float] | tuple[float, float, str]:
    """
    Richiede due numeri all'utente e, se richiesto, anche un'operazione.

    La funzione è riutilizzabile in diversi esercizi:
    può restituire solo i due numeri oppure anche l'operazione scelta.

    Args:
        con_operazione (bool): Se True, richiede anche un'operazione
            valida tra +, -, *, /, ** e %.

    Returns:
        tuple[float, float]: I due numeri inseriti dall'utente.
        tuple[float, float, str]: I due numeri e l'operazione scelta.
    """

    while True:
        valore = input("Inserisci il primo numero: ")

        if valore.isdigit():
            a = float(valore)
            break
        else:
            print("Errore: inserisci un numero valido")

    while True:
        valore = input("Inserisci il secondo numero: ")

        if valore.isdigit():
            b = float(valore)
            break
        else:
            print("Errore: inserisci un numero valido")

    if con_operazione:
        while True:
            operazione = input(
                "Scegli un'operazione (+, -, *, /, **, %): "
            )

            if operazione in ("+", "-", "*", "/", "**", "%"):
                return a, b, operazione
            else:
                print("Errore: inserisci un'operazione valida")

    return a, b

# -------------------------------------------------------------

# Obiettivi e regole

# Nel laboratorio applicherai:

#     Definizione e chiamata di funzioni.
#     Parametri, valori default e return.
#     Liste, cicli e funzioni utility.
#     Scope locale e assenza di global inutili.
#     *args, **kwargs.
#     Docstring e type hint.


# Attività 1 — Funzioni utility base
# Consegna

# Crea utility_base.py con tre funzioni:

#     saluta(nome): stampa un saluto.
#     quadrato(numero): restituisce il quadrato.
#     e_pari(numero): restituisce True se il numero è pari, altrimenti False.

# Chiama tutte le funzioni e stampa i risultati.
def esercizio_1():
    def saluta(nome: str) -> None:
        """
        Stampa un saluto personalizzato.

        Args:
            nome (str): Nome della persona da salutare.
        """
        print(f"Ciao {nome}!")

    def quadrato(numero: float) -> float:
        """
        Calcola il quadrato di un numero.

        Args:
            numero (float): Numero di cui calcolare il quadrato.

        Returns:
            float: Il quadrato del numero.
        """
        return numero ** 2

    def e_pari(numero: int) -> bool:
        """
        Verifica se un numero è pari.

        Args:
            numero (int): Numero da verificare.

        Returns:
            bool: True se il numero è pari, False altrimenti.
        """
        return numero % 2 == 0

    saluta("Alice")
    print(f"Quadrato di 5: {quadrato(5)}")
    print(f"10 è pari? {e_pari(10)}")




# Attività 2 — Utility su lista Guidata
# Consegna

# Crea utility_lista.py. Definisci:

#     somma_numeri(numeri): restituisce la somma degli elementi.
#     conta_pari(numeri): restituisce quanti elementi sono pari.

# Usa la lista:
# numeri = [3, 8, 11, 14, 20]

# Stampa entrambi i risultati.
def esercizio_2():
    def somma_numeri(numeri: list[int]) -> int:
        """
        Calcola la somma degli elementi di una lista.

        Args:
            numeri (list[int]): Lista di numeri interi.

        Returns:
            int: La somma degli elementi della lista.
        """
        return sum(numeri)

    def conta_pari(numeri: list[int]) -> int:
        """
        Conta quanti numeri pari sono presenti nella lista.

        Args:
            numeri (list[int]): Lista di numeri interi.

        Returns:
            int: Numero di elementi pari presenti nella lista.
        """
        return len([n for n in numeri if n % 2 == 0])

    numeri = [3, 8, 11, 14, 20]
    print(f"Somma: {somma_numeri(numeri)}")
    print(f"Numeri pari: {conta_pari(numeri)}")


# Attività 5 — Calcolatrice base a funzioni Autonoma
# Consegna

# Crea calcolatrice_base.py. Definisci quattro funzioni:
# somma(a, b)
# sottrai(a, b)
# moltiplica(a, b)
# dividi(a, b)

# Ogni funzione deve restituire il risultato con return.

# Fuori dalle funzioni, chiedi due numeri con float(input(...)) e stampa tutti e quattro i risultati.
def esercizio_3() -> None:
    """
    Esegue i calcoli base su due numeri inseriti dall'utente.

    Richiede due numeri e stampa il risultato di somma,
    sottrazione, moltiplicazione e divisione.
    """
    a, b = inserisci_dati()

    print(f"Somma: {somma(a, b)}")
    print(f"Sottrazione: {sottrai(a, b)}")
    print(f"Moltiplicazione: {moltiplica(a, b)}")
    print(f"Divisione: {dividi(a, b)}")






# Attività 6 — Somma variabile con *args Autonoma
# Consegna

# Crea somma_variabile.py. Definisci:
# somma_tutti(*numeri)

# La funzione deve:

#     Ricevere un numero variabile di valori.
#     Restituire la somma totale.
#     Restituire 0 se non riceve valori.

# Prove richieste
# print(somma_tutti())
# print(somma_tutti(5))
# print(somma_tutti(1, 2, 3, 4))
def esercizio_4() -> None:
    """
    Esegue alcuni test della funzione somma_tutti.
    """

    def somma_tutti(*numeri: int) -> int:
        """
        Somma un numero variabile di valori.

        Args:
            *numeri (int): Numeri interi da sommare.

        Returns:
            int: La somma dei numeri ricevuti.
                  Restituisce 0 se non vengono forniti valori.
        """
        return sum(numeri)

    print(somma_tutti())
    print(somma_tutti(5))
    print(somma_tutti(1, 2, 3, 4))



# Attività 7 — Calcolatrice estesa Sfida
# Consegna

# Crea calcolatrice_estesa.py. Il programma deve definire queste funzioni:
# somma(a, b)
# sottrai(a, b)
# moltiplica(a, b)
# dividi(a, b)
# potenza(a, b)
# resto(a, b)

# Il programma deve chiedere due numeri e un'operazione: +, -, *, /, **, %.

# Usa if / elif / else per chiamare la funzione corretta.
def esercizio_5() -> None:
    """
    Esegue un'operazione matematica scelta dall'utente.

    Richiede due numeri e un'operazione tra +, -, *, /, ** e %,
    quindi utilizza la funzione corrispondente e stampa il risultato.
    """
    a, b, operazione = inserisci_dati(con_operazione=True)

    if operazione == "+":
        risultato = somma(a, b)
    elif operazione == "-":
        risultato = sottrai(a, b)
    elif operazione == "*":
        risultato = moltiplica(a, b)
    elif operazione == "/":
        risultato = dividi(a, b)
    elif operazione == "**":
        risultato = potenza(a, b)
    elif operazione == "%":
        risultato = resto(a, b)
    else:
        print("Operazione non valida")
        return

    print(f"Risultato: {risultato}")






# Attività 8 — Sfida finale: report calcolatrice Difficile
# Consegna

# Estendi calcolatrice_estesa.py con una funzione:
# stampa_report(operazione, a, b, risultato, **dettagli)

# La funzione deve stampare un report con:

#     Operazione richiesta.
#     Primo e secondo numero.
#     Risultato.
#     Eventuali dettagli aggiuntivi ricevuti in **dettagli.

# Usa la funzione dopo avere calcolato il risultato.
def esercizio_6():
    def stampa_report(
        operazione: str,
        a: float,
        b: float,
        risultato: float,
        **dettagli: str
    ) -> None:
        """
        Stampa un report con i dati del calcolo.

        Args:
            operazione (str): Operazione eseguita.
            a (float): Primo numero.
            b (float): Secondo numero.
            risultato (float): Risultato del calcolo.
            **dettagli (str): Informazioni aggiuntive da mostrare.
        """

        print("\n--- Report Calcolatrice ---")
        print(f"Operazione: {operazione}")
        print(f"Primo numero: {a}")
        print(f"Secondo numero: {b}")
        print(f"Risultato: {risultato}")

        for chiave, valore in dettagli.items():
            print(f"{chiave}: {valore}")

        print("---------------------------\n")

    a, b, operazione = inserisci_dati(con_operazione=True)

    if operazione == "+":
        risultato = somma(a, b)
    elif operazione == "-":
        risultato = sottrai(a, b)
    elif operazione == "*":
        risultato = moltiplica(a, b)
    elif operazione == "/":
        risultato = dividi(a, b)
    elif operazione == "**":
        risultato = potenza(a, b)
    elif operazione == "%":
        risultato = resto(a, b)
    else:
        print("Operazione non valida")
        return

    stampa_report(
        operazione,
        a,
        b,
        risultato,
        note="Calcolo completato con successo"
    )


# MENU ESERCIZI
# -------------------------------------------------------------

ESERCIZI = {
    "esercizio_1": "Attività 1 — Funzioni utility base",
    "esercizio_2": "Attività 2 — Utility su lista",
    "esercizio_3": "Attività 5 — Calcolatrice base a funzioni",
    "esercizio_4": "Attività 6 — Somma variabile con *args",
    "esercizio_5": "Attività 7 — Calcolatrice estesa",
    "esercizio_6": "Attività 8 — Sfida finale: report calcolatrice"
}

while True:

    print("\n" + "=" * 60)
    print("MENU ESERCIZI")
    print("=" * 60)

    esercizi_disponibili = []

    for nome, descrizione in ESERCIZI.items():
        if callable(globals().get(nome)):
            esercizi_disponibili.append((nome, descrizione))

    for numero, esercizio in enumerate(esercizi_disponibili, 1):
        print(f"{numero}. {esercizio[1]}")

    print("0. Esci")

    scelta = input("Scegli un esercizio: ")

    if scelta == "0":
        print("Programma terminato")
        break

    try:
        scelta = int(scelta)
    except ValueError:
        print("Errore: scelta non valida")
        continue

    if scelta < 1 or scelta > len(esercizi_disponibili):
        print("Errore: esercizio non trovato")
        continue

    nome = esercizi_disponibili[scelta - 1][0]
    globals()[nome]()