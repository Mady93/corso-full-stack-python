import random
import math
from datetime import date


class Esercizi:

    def _mostra_risultato(self):
        """
        Stampa un'intestazione per separare visivamente l'input dal risultato dell'esercizio.
        """
        print("\nRisultato:")

    def esercizio_1(self):
        """
        Maggiore o minore
        Scrivi un programma che chiede all'utente di inserire due numeri interi e stampa quale dei due è maggiore.
        Esempio output: "Il numero maggiore è: 15"
        """

        a = input("Inserisci il primo numero: ")

        # isdigit() controlla se la stringa è composta solo da cifre (0-9): se non lo è, richiede di nuovo l'input
        while not a.isdigit():
            a = input("Inserisci un numero intero valido: ")

        # int() converte la stringa validata in numero intero
        a = int(a)

        b = input("Inserisci il secondo numero: ")

        while not b.isdigit():
            b = input("Inserisci un numero intero valido: ")

        b = int(b)

        # match-case confronta il valore della tupla (a, b) con i vari pattern "case"
        # ogni case può avere una condizione "if" (guard) che filtra quando quel case si applica
        match (a, b):
            # case (x, y) if x > y: assegna a=x, b=y e verifica la condizione x > y
            case (x, y) if x > y:
                self._mostra_risultato()
                print(f"Il numero maggiore è: {x}")

            case (x, y) if y > x:
                self._mostra_risultato()
                print(f"Il numero maggiore è: {y}")

            # case senza guard: cattura tutti i casi rimanenti (cioè x == y)
            case (x, y):
                self._mostra_risultato()
                print("I due numeri sono uguali")


    def esercizio_2(self):
        """
        Conto alla rovescia
        Scrivi un programma che chiede all'utente un numero intero positivo e stampa un conto alla rovescia da quel numero fino a 0.
        Requisiti:
        Esempio: se l'utente inserisce 5, stampa: 5, 4, 3, 2, 1, 0, BUUM!
        """

        n = input("Inserisci un numero intero positivo: ")

        # controlla che la stringa sia fatta di sole cifre E che il valore sia positivo (> 0)
        while not n.isdigit() or int(n) <= 0:
            n = input("Inserisci un numero intero positivo valido: ")

        n = int(n)

        # range(n, -1, -1): parte da n, si ferma prima di -1 (quindi arriva a 0), step -1 (decrescente)
        for i in range(n, -1, -1):
            self._mostra_risultato()
            # end=", " sostituisce l'a-capo di default di print con una virgola, così i numeri restano sulla stessa riga
            print(i, end=", ")

        print("BUUM!")


    def esercizio_4(self):
        """
        Valutazione voto
        Scrivi un programma che chiede all'utente un voto numerico (da 0 a 100) e stampa la valutazione corrispondente.
        Esempio: se l'utente inserisce 85, stampa "Ottimo"
        """
        v = input("Inserisci il voto: ")

        # ciclo infinito che si interrompe solo con break, usato per validare l'input in modo più flessibile di isdigit()
        while True:
            try:
                # float() converte la stringa in numero decimale; se non è un numero valido lancia ValueError
                v = float(v)

                # controlla che il voto sia nell'intervallo consentito, altrimenti richiede di nuovo l'input
                if 0 <= v <= 100:
                    break

            # se float(v) fallisce (stringa non numerica), l'eccezione viene "ignorata" con pass e si richiede input
            except ValueError:
                pass

            v = input("Inserisci un voto valido da 0 a 100: ")

        # catena di if/elif per assegnare la valutazione in base alle soglie del voto
        if v >= 85:
            self._mostra_risultato()
            print("Ottimo")
        elif v >= 80:
            self._mostra_risultato()
            print("Buono")
        elif v >= 70:
            self._mostra_risultato()
            print("Discreto")
        elif v >= 60:
            self._mostra_risultato()
            print("Sufficiente")
        else:
            self._mostra_risultato()
            print("Insufficiente")


    def esercizio_5(self):
        """
        Somma dei numeri pari
        Scrivi un programma che chiede all'utente un numero intero positivo N e calcola la somma di tutti i numeri pari da 0 a N (incluso).
        Esempio: se N=10, i numeri pari sono 0,2,4,6,8,10 e la somma è 30
        """

        n_ = input("Inserisci un numero intero positivo: ")

        while not n_.isdigit() or int(n_) <= 0:
            n_ = input("Inserisci un numero intero positivo valido: ")

        n_ = int(n_)

        # variabile accumulatore, inizializzata a 0 prima del ciclo
        somma_pari = 0

        # range(0, n_ + 1): da 0 a n_ incluso (per questo si somma +1 all'estremo superiore)
        for i in range(0, n_ + 1):
            # % è l'operatore modulo: restituisce il resto della divisione; se il resto diviso 2 è 0, il numero è pari
            if i % 2 == 0:
                print(f"I numeri pari sono: {i}")
                # += aggiunge i al valore corrente di somma_pari (equivale a somma_pari = somma_pari + i)
                somma_pari += i

        self._mostra_risultato()
        print(f"La somma dei numeri pari è: {somma_pari}")


    def esercizio_6(self):
        """
        Indovina il numero (con tentativi limitati)
        Scrivi un programma che fa indovinare all'utente un numero segreto (scegli tu un numero tra 1 e 20). 
        L'utente ha a disposizione 5 tentativi.
        """

        # random.randint(1, 20) genera un intero casuale compreso tra 1 e 20 (estremi inclusi)
        numero = random.randint(1, 20)

        # contatore dei tentativi effettuati
        c = 0

        # il ciclo continua finché non si arriva a 5 tentativi
        while c < 5:
            ins = input("Inserisci un numero intero da 1 a 20: ")

            # Finche quello che hai inserito non è un numero formato da cifre, continua a chiedere (not ins.isdigit())
            # qui si validano anche i limiti (< 1 o > 20)
            while not ins.isdigit() or int(ins) < 1 or int(ins) > 20:
                ins = input("Numero non valido. Inserisci un numero da 1 a 20: ")

            ins = int(ins)

            # incremento del contatore ad ogni tentativo valido
            c += 1

            if ins == numero:
                self._mostra_risultato()
                print("Hai indovinato!")
                # break interrompe subito il ciclo while, senza aspettare che c arrivi a 5
                break
            else:
                self._mostra_risultato()
                print(f"Numero non indovinato. Hai ancora {5 - c} tentativi.")

        # dopo il ciclo, se l'ultimo tentativo non è quello giusto, significa che i tentativi sono finiti
        if ins != numero:
            self._mostra_risultato()
            print(f"Hai esaurito i tentativi. Il numero era {numero}.")


    def esercizio_7(self):
        """
        Numeri primi fino a N
        Scrivi un programma che chiede all'utente un numero intero positivo N e stampa tutti i numeri primi da 2 a N.
        Esempio: se N=20, stampa: 2, 3, 5, 7, 11, 13, 17, 19
        """

        n = input("Numero: ")

        while not n.isdigit() or int(n) <= 0:
            n = input("Inserisci un numero intero positivo valido: ")

        n = int(n)

        # scorre tutti i numeri da 2 a n inclusi (i numeri primi partono da 2)
        for numero in range(2, n + 1):

            # variabile flag: si parte assumendo che il numero sia primo, e la si smentisce se si trova un divisore
            primo = True

            # I numeri minori o uguali a 1 non sono primi
            if numero <= 1:
                primo = False
            else:

                # Se numero è > di 1, cerco un eventuale divisore
                # I assume i valori da 2 fino alla radice quadrata di numero. math.sqrt(numero) calcola la radice quadrata
                # basta controllare fino alla radice quadrata perché eventuali divisori più grandi avrebbero già un "corrispondente" più piccolo trovato prima
                for i in range(2, int(math.sqrt(numero)) + 1):

                    # % calcola il resto della divisione. 25 % 5 = 0 non è un numero primo
                    if numero % i == 0:
                        primo = False
                        # break esce dal for interno appena si trova un divisore, non serve continuare a controllare
                        break

            if primo:
                self._mostra_risultato()
                print(numero)


    def esercizio_8(self):
        """
        Triangolo di asterischi
        Scrivi un programma che chiede all'utente un numero intero positivo N e stampa un triangolo di asterischi alto N righe.
        Esempio per N=5:
        *
        **
        ***
        ****
        *****
        """
        n = input("Inserisci un numero intero positivo: ")

        while not n.isdigit() or int(n) <= 0:
            n = input("Inserisci un numero intero positivo valido: ")

        n = int(n)

        # range(1, n + 1): da 1 a n, così alla riga i-esima corrisponde i asterischi
        for i in range(1, n + 1):
            self._mostra_risultato()
            # "*" * i è la ripetizione della stringa "*" per i volte (es. i=3 -> "***")
            print("*" * i)


    def esercizio_9(self):
        """
        Sequenza di Fibonacci
        Scrivi un programma che chiede all'utente quanti numeri della sequenza di Fibonacci vuole visualizzare e li stampa tutti.
        Esempio per 10 numeri: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
        """

        n = input("Quanti numeri della sequenza di Fibonacci vuole visualizzare? Es: (intero positivo) ")

        while not n.isdigit() or int(n) <= 0:
            n = input("Inserisci un numero intero positivo valido: ")

        n = int(n)

        # a e b sono i primi due termini della sequenza di Fibonacci
        a = 0
        b = 1

        # lista in cui accumulo i numeri della sequenza, invece di stamparli uno alla volta
        sequenza = []

        # il ciclo esegue n iterazioni (range(n) genera n valori, da 0 a n-1)
        for i in range(n):
            # str(a) converte il numero in stringa e lo aggiunge alla lista
            sequenza.append(str(a))
            # calcola il termine successivo come somma dei due precedenti
            somma = a + b
            # a prende il valore che aveva b (si "scorre" la sequenza di una posizione)
            a = b
            # b diventa il nuovo termine calcolato
            b = somma

        self._mostra_risultato()
        # ", ".join(sequenza) unisce tutti gli elementi della lista in un'unica stringa separata da ", ", senza virgola finale
        print(", ".join(sequenza))


    def esercizio_10(self):
        """
        Menu interattivo con continue e break
        Scrivi un programma che mostra un menu interattivo all'utente e continua a chiedere scelte finche l'utente non decide di uscire.

        Esempio menu:
        1. Saluta
        2. Stampa la data (usa una stringa fissa)
        3. Fai un calcolo (somma due numeri a scelta)
        4. Esci
        Il programma deve continuare finche l'utente non sceglie 4
        """

        # while True: ciclo infinito, si esce solo con il break dentro il case "4"
        while True:
            print("1. Saluta")
            print("2. Stampa la data")
            print("3. Fai un calcolo")
            print("4. Esci")

            menu = input("Scegli un'opzione: ")

            # match-case sulla stringa menu: confronta il valore inserito con ogni "case"
            match menu:
                case "1":
                    self._mostra_risultato()
                    print("Salve!")

                case "2":
                    self._mostra_risultato()
                    # date.today() restituisce la data odierna, strftime la formatta come giorno/mese/anno
                    print(date.today().strftime("%d/%m/%Y"))

                case "3":
                    n1 = input("Inserisci il primo numero: ")

                    # while True + try/except: ripete la richiesta finché la conversione a float non va a buon fine
                    while True:
                        try:
                            n1 = float(n1)
                            break
                        except ValueError:
                            n1 = input("Inserisci un numero valido: ")

                    n2 = input("Inserisci il secondo numero: ")

                    while True:
                        try:
                            n2 = float(n2)
                            break
                        except ValueError:
                            n2 = input("Inserisci un numero valido: ")
                            
                    self._mostra_risultato()
                    print(f"La somma è: {n1 + n2}")

                case "4":
                    self._mostra_risultato()
                    print("Uscita dal programma")
                    # break esce dal while True principale, terminando il menu
                    break

                # case _: è il caso di default, cattura qualsiasi valore che non ha fatto match con i case precedenti
                case _:
                    self._mostra_risultato()
                    print("Scelta non valida")


# Creo un oggetto della classe
esercizi = Esercizi()

# dir(esercizi) restituisce la lista di tutti i nomi (attributi e metodi) dell'oggetto
# il filtro "if nome.startswith('esercizio_')" tiene solo i metodi che iniziano con quel prefisso, escludendo _mostra_risultato e altri metodi "interni"
# nome.split("_")[1] estrae la parte numerica dopo l'underscore (es. da "esercizio_9" ottiene "9"), usata come chiave del dizionario
# getattr(esercizi, nome) recupera il metodo vero e proprio a partire dal suo nome in stringa
metodi = {
    nome.split("_")[1]: getattr(esercizi, nome)
    for nome in dir(esercizi)
    if nome.startswith("esercizio_")
}

# sorted(metodi.items(), key=lambda coppia: int(coppia[0])) ordina le chiavi numericamente (altrimenti "10" finirebbe prima di "2" come stringa)
# dict(...) ricostruisce un dizionario ordinato a partire dalla lista di coppie ordinate
metodi = dict(sorted(metodi.items(), key=lambda coppia: int(coppia[0])))


# try/except attorno al ciclo: se l'utente preme Ctrl+C, invece del traceback viene gestito il KeyboardInterrupt
try:
    # ciclo infinito: continua a chiedere quale esercizio eseguire finché l'utente non digita "esci"
    while True:
        # riga vuota + separatore prima di ogni nuova richiesta, per staccare visivamente dall'output precedente
        print("\n" + "-" * 130)

        # ', '.join(metodi.keys()) unisce tutte le chiavi del dizionario in una stringa separata da virgole, per mostrarle nel prompt
        scelta = input(f"Quale esercizio vuoi eseguire? ({', '.join(metodi.keys())}) oppure 'esci': ")

        print("-" * 130)

        # riga vuota dopo la scelta, per separare il prompt dall'output dell'esercizio
        print()

        # se l'utente digita "esci", break interrompe il while True e termina il programma
        if scelta == "esci":
            break

        # in metodi controlla se la stringa inserita è una delle chiavi del dizionario
        if scelta in metodi:
            # metodi[scelta] cerca nel dizionario la funzione associata alla chiave "scelta"
            # le parentesi () subito dopo sono quelle che effettivamente avviano l'esecuzione della funzione
            metodi[scelta]()
        else:
            print("Esercizio non valido")

# se durante il while True l'utente preme Ctrl+C,
# questo blocco intercetta l'interruzione ed evita il traceback
except KeyboardInterrupt:
    # \n (va a capo)
    print("\nProgramma interrotto dall'utente.")