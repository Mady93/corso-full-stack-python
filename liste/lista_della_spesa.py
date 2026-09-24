class Esercizi:

    def _mostra_risultato(self):
        print()

    def __init__(self):
        self.lista = []
        self.backup = []

    def esercizio_1(self):
        """
        Scenario Reale
        Sei stato assunto da un supermercato online per creare un sistema di gestione della lista della spesa. 
        Il sistema deve permettere agli utenti di aggiungere prodotti, rimuoverli, cercarli, 
        ordinare la lista e ottenere statistiche sugli articoli presenti.

        Consegna
        Crea un programma Python completo che gestisca una lista della spesa interattiva. 
        Il programma deve permettere all'utente di eseguire tutte le operazioni principali su una lista 
        attraverso un menu testuale.

        EXTRA
        Impedisci duplicati quando aggiungi un prodotto
        Mostra un messaggio se si cerca di rimuovere un prodotto che non esiste
        Aggiungi un'operazione per sostituire un prodotto con un altro
        Salva la lista in una variabile di backup prima di operazioni distruttive

        """

        self.lista
        self.backup

        while True:
            print("\n" + "-" * 60)
            print("1. Add product")
            print("2. Remove product")
            print("3. Search product")
            print("4. Sort list")
            print("5. Statistics products")
            print("6. Replace product")
            print("7. Remove all products")
            print("8. Display products")
            # print("9. Restore backup")
            # print("10. Partial search")
            # print("11. Filter products")
            # print("12. Filter products")
            # print("13. Count products by initial")
            print("9. Exit menu")
            print("\n" + "-" * 60)
        
            menu = input("Choose an option: ")
            #print(f"DEBUG: menu = {repr(menu)}")
        
            match menu:
                case "1":
                    while True:
                        self._mostra_risultato()
                        prodotto = input("Enter product name: ")

                        if prodotto.lower() in [p.lower() for p in self.lista]:
                            self._mostra_risultato()
                            print("Product already exists")
                        else:
                            self.lista.append(prodotto)
                            self._mostra_risultato()
                            print(f"Product added successfully {self.lista}")

                        scelta = input(
                        "Do you want to add another product? "
                        "(y = continue, n = return to menu): ")

                        if scelta == "n":
                            break
        
                case "2":
                    while True:
                        self._mostra_risultato()
                        prodotto = input("Enter product name: ")

                        if prodotto in self.lista:
                            self.backup = self.lista.copy()
                            self.lista.remove(prodotto)
                            print(f"Product removed successfully {self.lista}")
                        else:
                            print("Product not found")

                        scelta = input(
                        "Do you want to remove another product? "
                        "(y = continue, n = return to menu): ")
                    
                        if scelta == "n":
                            break
        
                case "3":
                    while True:
                        self._mostra_risultato()
                        prodotto = input("Enter product name: ")
                    
                        if prodotto.lower() in [p.lower() for p in self.lista]:
                            print(f"Product found: {prodotto}")
                        else:
                            print("Product not found")
                    
                        scelta = input(
                        "Do you want to search another product? "
                        "(y = continue, n = return to menu): ")
                    
                        if scelta == "n":
                            break
        
                case "4":
                    self._mostra_risultato()

                    if self.lista:
                        self.lista.sort()
                        print(f"Products sorted successfully: {self.lista}")
                    else:
                        print("No products have been added yet")
 
                case "5":
                    self._mostra_risultato()
                    print(f"Total products: {len(self.lista)}")

                    if self.lista:
                        print(f"First added: {self.lista[0]}")
                        print(f"Last added: {self.lista[-1]}")
                        print(f"Unique products: {len(set(self.lista))}")
                    else:
                        print("No products have been added yet")

                case "6":
                    self._mostra_risultato()
                    prodotto_vecchio = input("Which product do you want to replace? ")

                    if prodotto_vecchio.lower() in [p.lower() for p in self.lista]:
                        self._mostra_risultato()
                        prodotto_nuovo = input("What do you want to replace it with? ")

                        if prodotto_nuovo.lower() in [p.lower() for p in self.lista]:
                            self._mostra_risultato()
                            print("Product already exists")

                        else:
                            indice = next(
                                i for i, p in enumerate(self.lista)   
                                if p.lower() == prodotto_vecchio.lower()
                            )

                            self.backup = self.lista.copy()
                            self.lista[indice] = prodotto_nuovo

                            self._mostra_risultato()
                            print(f"Product replaced successfully: {self.lista}")
                    else:
                        self._mostra_risultato()
                        print("Product not found")

                        scelta = input("Do you want to add this product? (y/n): ")

                        if scelta == "y":
                            self.lista.append(prodotto_vecchio)
                            self._mostra_risultato()
                            print(f"Product added successfully: {self.lista}")

                case "7":
                    self._mostra_risultato()
                    self.backup = self.lista.copy()
                    self.lista.clear()
                    print(f"All products removed successfully: {self.lista}")
                
                case "8":
                    self._mostra_risultato()

                    if self.lista:
                        print(f"Products retrieved successfully: {self.lista}")
                    else:
                        print("No products have been added yet")

                case "9":
                    self._mostra_risultato()
                    print("Menu closed")
                    break

                    

        

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
        scelta = input(f"Which exercise would you like to run? [{', '.join(metodi.keys())}] or 'exit': ")

        print("-" * 130)

        # riga vuota dopo la scelta, per separare il prompt dall'output dell'esercizio
        print()

        # se l'utente digita "exit", break interrompe il while True e termina il programma
        if scelta == "exit":
            print("Program closed")
            break

        # in metodi controlla se la stringa inserita è una delle chiavi del dizionario
        if scelta in metodi:
            # metodi[scelta] cerca nel dizionario la funzione associata alla chiave "scelta"
            # le parentesi () subito dopo sono quelle che effettivamente avviano l'esecuzione della funzione
            metodi[scelta]()
        else:
            print("Invalid exercise")

# se durante il while True l'utente preme Ctrl+C,
# questo blocco intercetta l'interruzione ed evita il traceback
except KeyboardInterrupt:
    print("-" * 130)
    # \n (va a capo)
    print("\nProgram closed")