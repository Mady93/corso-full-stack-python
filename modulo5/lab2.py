# Esercizio finale
# Realizza un gioco testuale in Python

# Scegli liberamente il tema del gioco: avventura, investigazione, sopravvivenza, quiz, corse automobilistiche, gestione squadra o altro.

#     Schermata iniziale con titolo e istruzioni
#     Profilo giocatore con nome, punteggio, vite o energia e inventario
#     Scelte dell'utente tramite input()
#     Ciclo principale fino a vittoria, sconfitta o uscita
#     Schermata finale con risultato e dati del giocatore

# Consegna: file Python eseguibile da terminale. 


"""
CHI NASCONDE IL FRAMMENTO?

Gioco testuale a tema InuYasha
--------------------------

TRAMA
-----

Un frammento della Sacra Perla è caduto in un villaggio.
Naraku ha mandato un servo youkai mutaforma, travestito da
uno dei tre abitanti del villaggio, per rubarlo prima di voi.

Dovete scoprire chi, tra i tre sospettati, è in realtà il
mutaforma prima che il Kazaana di Miroku si allarghi troppo.

COME SI GIOCA
-------------

- All'inizio viene fornito un fatto certo:
  il luogo e il colore dell'abito del mutaforma visto all'alba.

- Ad ogni turno puoi scegliere di:

    1) Interrogare un sospettato.
       Ogni sospettato può essere interrogato una sola volta.

    2) Chiedere a Kagome di verificare un sospettato.
       Kagome può essere usata una sola volta.

    3) Fare l'accusa finale.

    4) Mostrare il profilo.

    0) Uscire dal gioco.

- Ogni interrogatorio consuma 1 punto di energia.

- Kagome consuma 2 punti di energia.

- Se l'energia arriva a 0 prima dell'accusa,
  il giocatore perde.

- Se l'accusa è corretta, il giocatore vince.

- Se l'accusa è sbagliata, il giocatore perde.

Eseguire con Python.
"""

# Energia iniziale
ENERGIA_MASSIMA = 6

# Costi delle azioni
COSTO_INTERROGATORIO = 1
COSTO_KAGOME = 2

# Questo è l'indizio che il giocatore conosce già all'inizio
# Serve per confrontare i sospettati
FATTO_INIZIALE = {
    "luogo": "fiume",
    "colore": "verde"
}


# Informazioni dei tre sospettati
# Yuki è il mutaforma della partita
SOSPETTATI = {
    "1": {
        "nome": "Aiko",
        "luogo": "mercato",
        "colore": "rosso",
        "mutaforma": False,
        "dichiarazione":
            "Stamattina ero al mercato a vendere riso, vestivo di rosso."
    },

    "2": {
        "nome": "Genzo",
        "luogo": "fiume",
        "colore": "blu",
        "mutaforma": False,
        "dichiarazione":
            "Stamattina ero al fiume a pescare, vestivo di blu."
    },

    "3": {
        "nome": "Yuki",
        "luogo": "fiume",
        "colore": "verde",
        "mutaforma": True,
        "dichiarazione":
            "Stamattina ero al fiume a raccogliere acqua, vestivo di verde."
    }
}



# SCHERMATA INIZIALE

def mostra_titolo_e_istruzioni() -> None:
    """
    Mostra il titolo, la trama e le istruzioni del gioco.
    """

    print("=" * 60)
    print("        CHI NASCONDE IL FRAMMENTO?")
    print("        Un mistero nello Sengoku")
    print("=" * 60)

    print("""
Un frammento della Sacra Perla è nascosto nel villaggio.

Un servo mutaforma di Naraku si è travestito da uno dei
tre abitanti per rubarlo prima di voi.

OBIETTIVO:
Scoprire quale dei tre sospettati è il mutaforma.

COME SI GIOCA:

1) Interroga i sospettati e raccogli le loro dichiarazioni.

2) Confronta luogo e colore dell'abito con il fatto iniziale.

3) Puoi chiedere a Kagome di verificare un sospettato.
   Puoi usare questa possibilità una sola volta.

4) Puoi controllare il tuo profilo.

5) Quando sei pronto, puoi fare l'accusa finale.

6) Se l'accusa è corretta, vinci.

7) Se l'accusa è sbagliata, perdi.

ATTENZIONE:
Ogni interrogatorio consuma energia.
Kagome consuma 2 punti energia.

Se l'energia arriva a 0 prima dell'accusa,
il Kazaana di Miroku si allarga troppo e perdi.
""")

    print("=" * 60)


# PROFILO GIOCATORE
def crea_profilo() -> dict:
    """
    Crea il profilo iniziale del giocatore.

    Returns:
        dict: Profilo del giocatore.
    """

    nome = input("\nCome ti chiami, viaggiatore? ")

    # Se non viene scritto niente uso un nome predefinito
    if nome == "":
        nome = "Viaggiatore"

    # Qui salvo tutti i dati che servono durante la partita
    profilo = {
        "nome": nome,
        "energia": ENERGIA_MASSIMA,
        "punteggio": 0,
        # Lista degli indizi trovati durante gli interrogatori
        "indizi": [],
        # Sospettati già interrogati
        "interrogati": [],
        # Serve per ricordare se Kagome è già stata usata
        "kagome_usata": False,
        # Numero delle azioni fatte dal giocatore
        "turni": 0
    }

    return profilo


def mostra_profilo(profilo: dict) -> None:
    """
    Mostra le informazioni del giocatore.

    Args:
        profilo (dict): Dati del giocatore.
    """

    print("\n" + "-" * 40)
    print("PROFILO GIOCATORE")
    print("-" * 40)

    print(f"Nome: {profilo['nome']}")
    print(
        f"Energia: {profilo['energia']}/{ENERGIA_MASSIMA}"
    )
    print(f"Punteggio: {profilo['punteggio']}")
    print(f"Turni giocati: {profilo['turni']}")

    print("\nIndizi raccolti:")

    # Se non ci sono indizi lo comunico al giocatore
    if len(profilo["indizi"]) == 0:
        print("- Nessun indizio raccolto.")
    else:
        # Mostro tutti gli indizi raccolti
        for indizio in profilo["indizi"]:
            print(f"- {indizio}")

    print("-" * 40)


# INTERROGATORIO

def interroga_sospettato(
    profilo: dict,
    numero: str
) -> None:
    """
    Interroga un sospettato.

    Il sospettato può essere interrogato una sola volta.

    Args:
        profilo (dict): Dati del giocatore.
        numero (str): Numero del sospettato.
    """

    # Prendo i dati del sospettato scelto
    sospettato = SOSPETTATI[numero]
    nome = sospettato["nome"]

    # Controllo se è già stato interrogato
    if numero in profilo["interrogati"]:

        print(f"\nHai già interrogato {nome}.")
        print("Non ci sono nuove informazioni.")

    else:

        # Controllo che il giocatore abbia ancora energia
        if profilo["energia"] <= 0:

            print("\nNon hai più energia.")
            print("Non puoi interrogare nessuno.")

        else:
            # Salvo il sospettato tra quelli già interrogati
            profilo["interrogati"].append(numero)

            # Ogni interrogatorio costa 1 energia
            profilo["energia"] -= COSTO_INTERROGATORIO

            print("\n" + "-" * 40)
            print(f"INTERROGATORIO DI {nome.upper()}")
            print("-" * 40)

            print(f"{nome} dice:")
            print(f"\"{sospettato['dichiarazione']}\"")

            # Creo un indizio con luogo e colore dichiarati
            indizio = (
                f"{nome}: "
                f"{sospettato['luogo']} - "
                f"{sospettato['colore']}"
            )

            # Aggiungo l'indizio al profilo
            profilo["indizi"].append(indizio)

            # Ogni interrogatorio dà 10 punti
            profilo["punteggio"] += 10

            print("\nIndizio aggiunto al profilo.")
            print("Hai guadagnato 10 punti.")
            print(
                f"Energia rimasta: {profilo['energia']}"
            )


# KAGOME

def usa_kagome(profilo: dict) -> None:
    """
    Permette a Kagome di controllare un sospettato.

    Kagome può essere utilizzata una sola volta.

    Args:
        profilo (dict): Dati del giocatore.
    """

    # Controllo se Kagome è già stata utilizzata
    if profilo["kagome_usata"]:

        print("\nHai già utilizzato il potere di Kagome.")

    else:

        # Kagome richiede 2 punti di energia
        if profilo["energia"] < COSTO_KAGOME:

            print("\nNon hai abbastanza energia.")
            print("Kagome non può utilizzare il suo potere.")

        else:

            print("\nKagome può controllare un sospettato.")

            print("\nScegli chi controllare:")

            # Mostro la lista dei sospettati
            for numero, sospettato in SOSPETTATI.items():
                print(
                    f"{numero}) {sospettato['nome']}"
                )

            scelta = input("Scelta: ")

            # Controllo che la scelta esista
            if scelta in SOSPETTATI:

                # Segno Kagome come già utilizzata
                profilo["kagome_usata"] = True

                # Uso 2 punti di energia
                profilo["energia"] -= COSTO_KAGOME

                sospettato = SOSPETTATI[scelta]

                print("\nKagome concentra i suoi poteri...")
                print("Il frammento della Sfera reagisce!")

                # Kagome dice direttamente se il sospettato è il mutaforma
                if sospettato["mutaforma"]:

                    print(
                        f"\nKagome: "
                        f"Avverto una presenza demoniaca!"
                    )

                    print(
                        f"{sospettato['nome']} "
                        f"è il mutaforma!"
                    )

                else:

                    print(
                        f"\nKagome: "
                        f"Non avverto alcuna presenza demoniaca."
                    )

                    print(
                        f"{sospettato['nome']} "
                        f"non è il mutaforma."
                    )

                # Aiuto di Kagome = 5 punti
                profilo["punteggio"] += 5

                print("Hai guadagnato 5 punti.")
                print(
                    f"Energia rimasta: {profilo['energia']}"
                )

            else:

                print("\nScelta non valida.")
                print("Kagome non utilizza il suo potere.")


# ACCUSA FINALE

def fai_accusa(profilo: dict) -> bool:
    """
    Permette al giocatore di accusare un sospettato.

    Args:
        profilo (dict): Dati del giocatore.

    Returns:
        bool: True se la partita deve terminare,
              False se l'accusa viene annullata.
    """

    print("\n" + "-" * 40)
    print("ACCUSA FINALE")
    print("-" * 40)

    print("\nChi pensi sia il mutaforma?")

    # Mostro i sospettati tra cui scegliere
    for numero, sospettato in SOSPETTATI.items():
        print(
            f"{numero}) {sospettato['nome']}"
        )

    print("0) Annulla")

    scelta = input("La tua accusa: ")

    # 0 permette di tornare al menu senza perdere
    if scelta == "0":

        print("\nHai deciso di aspettare ancora.")
        return False

    # Controllo che il numero inserito sia valido
    if scelta not in SOSPETTATI:

        print("\nScelta non valida.")
        return False

    sospettato = SOSPETTATI[scelta]

    # Controllo se il sospettato scelto è il mutaforma
    if sospettato["mutaforma"]:

        print("\n" + "=" * 60)
        print("                    VITTORIA!")
        print("=" * 60)

        print(
            f"\nHai scoperto che {sospettato['nome']} "
            f"è il mutaforma!"
        )

        print(
            "Il frammento della Sacra Perla "
            "è stato recuperato."
        )

        
        # Punti ottenuti per aver risolto il caso
        profilo["punteggio"] += 30

        # Bonus se il giocatore non ha chiesto aiuto a Kagome
        if profilo["kagome_usata"] == False:
            profilo["punteggio"] += 20
            print(
                "\nBonus: hai risolto il mistero "
                "senza l'aiuto di Kagome!"
            )

        print(
            f"\nPunteggio finale: "
            f"{profilo['punteggio']}"
        )

        print(
            f"Energia rimasta: "
            f"{profilo['energia']}"
        )

        return True

    else:

        print("\n" + "=" * 60)
        print("                    SCONFITTA")
        print("=" * 60)

        print(
            f"\nHai accusato {sospettato['nome']}, "
            "ma hai sbagliato."
        )

        print(
            "Il vero mutaforma riesce a fuggire "
            "con il frammento."
        )

        # Se l'accusa è sbagliata il punteggio diventa 0
        profilo["punteggio"] = 0

        print("\nPunteggio finale: 0")

        return True


# MENU

def mostra_menu() -> None:
    """
    Mostra il menu principale del gioco.
    """

    print("\n" + "-" * 50)
    print("MENU")
    print("-" * 50)

    print("1) Interroga Aiko")
    print("2) Interroga Genzo")
    print("3) Interroga Yuki")
    print("4) Chiedi aiuto a Kagome")
    print("5) Fai l'accusa finale")
    print("6) Mostra il profilo")
    print("0) Esci dal gioco")

    print("-" * 50)


# GIOCO

def gioca() -> None:
    """
    Gestisce il ciclo principale del gioco.
    """

    # Mostro la schermata iniziale
    mostra_titolo_e_istruzioni()

    # Creo il profilo del giocatore
    profilo = crea_profilo()

    # Mostro il primo indizio dato dalla storia
    print("\n" + "-" * 50)
    print("IL FATTO CERTO")
    print("-" * 50)

    print(
        f"\nUn abitante ha visto il mutaforma "
        f"all'alba vicino al {FATTO_INIZIALE['luogo']}."
    )

    print(
        f"Indossava un abito di colore "
        f"{FATTO_INIZIALE['colore']}."
    )

    print(
        "\nQuesto è un FATTO CERTO."
        "\nNon è una dichiarazione di un sospettato."
    )

    # Il gioco continua finché non c'è vittoria, sconfitta o uscita
    while True:

        # Se finisce l'energia il giocatore perde
        if profilo["energia"] <= 0:

            print("\n" + "=" * 60)
            print("                    SCONFITTA")
            print("=" * 60)

            print(
                "\nIl Kazaana di Miroku si è allargato troppo!"
            )

            print(
                "Miroku viene risucchiato e il "
                "mutaforma riesce a fuggire."
            )

            print(
                f"\nPunteggio finale: "
                f"{profilo['punteggio']}"
            )

            break

        # Mostro il menu ad ogni turno
        mostra_menu()

        # Leggo la scelta del giocatore
        scelta = input("Scegli un'azione: ")

        if scelta == "1":

            interroga_sospettato(
                profilo,
                "1"
            )

            profilo["turni"] += 1

        elif scelta == "2":

            interroga_sospettato(
                profilo,
                "2"
            )

            profilo["turni"] += 1

        elif scelta == "3":

            interroga_sospettato(
                profilo,
                "3"
            )

            profilo["turni"] += 1

        elif scelta == "4":

            usa_kagome(profilo)

            profilo["turni"] += 1

        elif scelta == "5":

            # L'accusa può terminare la partita oppure essere annullata
            fine_partita = fai_accusa(profilo)

            if fine_partita:

                break

        elif scelta == "6":

            # Mostra il profilo senza consumare energia
            mostra_profilo(profilo)

        # Il giocatore può uscire in qualsiasi momento
        elif scelta == "0":

            print("\nHai deciso di abbandonare la ricerca.")

            print(
                "Il frammento rimane nascosto "
                "nel villaggio."
            )

            # Se il numero non è nel menu, chiedo di riprovare
            print(
                f"\nPunteggio finale: "
                f"{profilo['punteggio']}"
            )

            break

        else:

            print(
                "\nScelta non valida."
                "\nInserisci uno dei numeri presenti nel menu."
            )


# AVVIO
gioca()
