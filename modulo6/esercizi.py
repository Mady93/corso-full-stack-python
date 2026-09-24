# Mini esercizio: import e alias
# Consegna

# Crea import_esercizio.py.

#     Importa il modulo math.
#     Calcola e stampa:
#         La radice quadrata di 144.
#         Il seno di math.pi / 2.
#         Il valore di math.e.
#     Rifai lo stesso esercizio importando solo sqrt e pi con from ... import.
#     Rifai ancora usando un alias per math.



# ESERCIZIO 1 - Importare il modulo math
def esercizio_1():
    """
    Esegue i calcoli importando l'intero modulo 'math'.
    
    In questo approccio, ogni volta che si vuole usare una funzione
    o una costante del modulo, bisogna prefissarla con 'math.' 
    (es. math.sqrt, math.pi).
    """
    import math

    # math.sqrt(x) calcola la radice quadrata di x
    print("Radice quadrata di 144:", math.sqrt(144))
    
    # math.sin(x) calcola il seno dell'angolo x (in radianti)
    # math.pi e' la costante Pi Greco (3.14159...)
    print("Seno di pi/2:", math.sin(math.pi / 2))
    
    # math.e e' la costante di Nepero (2.71828...)
    print("Valore di e:", math.e)


# ESERCIZIO 2 - Importare solo alcune funzioni/costanti
def esercizio_2():
    """
    Esegue i calcoli importando direttamente specifiche funzioni e costanti dal modulo 'math'.
    
    Usando la sintassi 'from math import ...', gli elementi importati
    vengono inseriti nello spazio dei nomi locale, quindi si possono usare 
    direttamente senza scrivere 'math.' davanti.
    """
    from math import sqrt, pi, sin, e

    # Usiamo sqrt() direttamente invece di math.sqrt()
    print("Radice quadrata di 144:", sqrt(144))
    
    # Usiamo sin() e pi direttamente
    print("Seno di pi/2:", sin(pi / 2))
    
    # Usiamo e direttamente
    print("Valore di e:", e)


# ESERCIZIO 3 - Usare un alias
def esercizio_3():
    """
    Esegue i calcoli importando il modulo 'math' con un alias (soprannome).
    
    La sintassi 'import math as m' rinomina momentaneamente il modulo in 'm'.
    E' molto utile per risparmiare tempo nella digitazione o con moduli dai nomi lunghi.
    """
    import math as m

    # Usiamo 'm.' al posto di 'math.'
    print("Radice quadrata di 144:", m.sqrt(144))
    print("Seno di pi/2:", m.sin(m.pi / 2))
    print("Valore di e:", m.e)



# Mini esercizio: uso combinato
# Consegna

# Crea esempio_moduli.py.
#
# Importa math, random e datetime.
# Calcola l'area di un cerchio con raggio casuale tra 1 e 10.
# Stampa la data e ora corrente.
# Calcola la data tra 7 giorni.
# Calcolare la vostra eta esatta.

def esercizio_4():
    """
    Esegue un esercizio sull'uso combinato dei moduli math, random e datetime.

    Calcola l'area di un cerchio con un raggio casuale,
    mostra la data e l'ora corrente, calcola la data tra 7 giorni
    e calcola l'età esatta in anni, mesi e giorni.
    """

    from math import pi
    from random import randint
    from datetime import datetime, timedelta
    from calendar import monthrange

    # Genero un raggio casuale tra 1 e 10
    raggio = randint(1, 10)

    # Calcolo l'area del cerchio usando pi greco
    area = pi * raggio ** 2

    print("Raggio:", raggio)
    print("Area del cerchio:", area)

    # Prendo la data e l'ora attuale
    adesso = datetime.now()

    # %d/%m/%Y %H:%M:%S indica come voglio visualizzare la data
    print("Data e ora corrente:", adesso.strftime("%d/%m/%Y %H:%M:%S"))

    # Aggiungo 7 giorni alla data attuale
    tra_7_giorni = adesso + timedelta(days=7)

    print("Data tra 7 giorni:", tra_7_giorni.strftime("%d/%m/%Y %H:%M:%S"))

    # Inserisco la mia data di nascita
    data_nascita = datetime(1993, 9, 4)

    # Calcolo gli anni compiuti
    anni = adesso.year - data_nascita.year

    # Se il compleanno non è ancora passato, tolgo un anno
    if (adesso.month, adesso.day) < (data_nascita.month, data_nascita.day):
        anni = anni - 1

    # Calcolo la data dell'ultimo compleanno
    # ultimo_compleanno = datetime(
    #     data_nascita.year + anni,
    #     data_nascita.month,
    #     data_nascita.day
    # )

    # # Calcolo quanti mesi e giorni sono passati dall'ultimo compleanno
    # mesi = adesso.month - ultimo_compleanno.month
    # giorni = adesso.day - ultimo_compleanno.day

    mesi = adesso.month - data_nascita.month
    giorni = adesso.day - data_nascita.day

    # Se il giorno di oggi è minore del giorno di nascita,
    # significa che non siamo ancora arrivati allo stesso giorno del mese del compleanno
    if giorni < 0:

        # Siccome non abbiamo ancora raggiunto quel giorno, togliamo un mese dal calcolo
        mesi = mesi - 1

        # Prendiamo il mese precedente rispetto a quello attuale
        # Serve per sapere quanti giorni dobbiamo aggiungere
        mese_precedente = adesso.month - 1

        # Se siamo a gennaio, il mese precedente è dicembre dell'anno precedente
        if mese_precedente == 0:
            mese_precedente = 12
            anno_precedente = adesso.year - 1

        # Negli altri casi l'anno rimane quello attuale
        else:
            anno_precedente = adesso.year

        # Calcoliamo quanti giorni ci sono nel mese precedente
        # Facciamo la differenza tra il primo giorno del mese successivo e il primo giorno del mese precedente
        # giorni_mese_precedente = (
        #     datetime(anno_precedente, mese_precedente + 1, 1)
        #     - datetime(anno_precedente, mese_precedente, 1)
        # ).days

        giorni_mese_precedente = monthrange(anno_precedente, mese_precedente)[1]

        # I giorni iniziali erano negativi
        # Aggiungendo i giorni reali del mese precedente otteniamo il numero corretto di giorni.
        giorni = giorni + giorni_mese_precedente

    # Se il calcolo dei mesi è negativo, torno indietro di un anno
    if mesi < 0:
        mesi = mesi + 12

    print("Data di nascita:", data_nascita.strftime("%d/%m/%Y"))
    print("Età:", anni, "anni,", mesi, "mesi e", giorni, "giorni")

   
    # weekday() restituisce da 0 (lunedì) a 6 (domenica)
    if data_nascita.weekday() <= 4:
        print("Sono nato in un giorno feriale")
    else:
        print("Sono nato nel weekend")






# Mini esercizio: crea il tuo modulo
# Consegna

# Crea un modulo 
# geometria.py
#  con:

# Una funzione per l'area del triangolo.
# Una funzione per l'area del rettangolo.
# Una funzione per l'area del cerchio.
# Una docstring di modulo e docstring per ogni funzione.
# Calcolatore di Aree "Universale"
# Poi crea main_geometria.py che importa e usa queste funzioni. 
def esercizio_5():
    """
    Usa il calcolatore universale delle aree.
    """

    from geometria import calcola_area

    area_triangolo = calcola_area("triangolo", 10, 5)
    area_rettangolo = calcola_area("rettangolo", 10, 5)
    area_cerchio = calcola_area("cerchio", 5)

    print("Area triangolo:", area_triangolo)
    print("Area rettangolo:", area_rettangolo)
    print("Area cerchio:", area_cerchio)







# MENU
while True:
    print("\n" + "=" * 60)
    print("MENU ESERCIZI")
    print("=" * 60)

    print("1. Importo tutto il modulo math")
    print("2. Importo solo quello che mi serve dal modulo math")
    print("3. Importo math usando l'alias m")
    print("4. Moduli (math, random, datetime)")
    print ("5. Calcolatore di Aree 'Universale'")
    print("0. Esci")

    scelta = input("Scegli un esercizio: ")

    match scelta:

        case "1":
            esercizio_1()

        case "2":
            esercizio_2()

        case "3":
            esercizio_3()

        case "4":
            esercizio_4()

        case "5":
            esercizio_5()

        case "0":
            print("Programma terminato")
            break

        case _:
            print("Errore: scelta non valida")