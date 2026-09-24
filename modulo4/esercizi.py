import json

# ---------------------------------------------------------
# Vincoli comuni

#     Usare nomi di variabili descrittivi.
#     Evitare variabili globali non necessarie.
#     Controllare gli input dell'utente.
#     Non interrompere il programma a causa di un dato non valido.
#     Stampare risultati leggibili e organizzati.
#     Usare break e continue solo quando migliorano la logica.
#     Aggiungere almeno un esempio di pass per una funzionalità futura.
# ---------------------------------------------------------


# ---------------------------------------------------------
# 1. Convertitore di unità

# Scrivere un programma che chieda all'utente una temperatura e l'unità di partenza.

# Il programma deve consentire le conversioni:

#     Celsius → Fahrenheit;
#     Fahrenheit → Celsius;
#     Celsius → Kelvin;
#     Kelvin → Celsius.

# Verificare che l'unità sia valida, impedire temperature Kelvin negative
# e stampare il risultato con due cifre decimali.

# Temperatura: 25
# Unità di partenza: C
# Risultato: 77.00 F
# ---------------------------------------------------------

"""
Two loops. The first validates the input (numeric temperature, unit in
C/F/K, no negative Kelvin) and exits with break only when everything is
correct, so the validated values stay available afterwards.
 
The second loop is the conversion menu: match selects the conversion and
each case checks that it is compatible with the starting unit. Invalid
options only print a message, so the menu ends only with option 5.
"""
while True:
    try:
        temperatura = float(input("Temperatura: "))
        unita = input("Unità di partenza (C/F/K): ").upper()

        if unita not in ["C", "F", "K"]:
            print("Unità non valida. Inserisci C, F oppure K")
            continue

        if unita == "K" and temperatura < 0:
            print("La temperatura in Kelvin non può essere negativa")
            continue

        break

    except ValueError:
        print("Temperatura non valida. Inserisci un numero")

while True:
    print("\n--- Scegli una conversione ---")
    print("1. Celsius → Fahrenheit")
    print("2. Fahrenheit → Celsius")
    print("3. Celsius → Kelvin")
    print("4. Kelvin → Celsius")
    print("5. Uscire")

    scelta = input("Scelta: ")

    match scelta:
        case "1":
            if unita == "C":
                risultato = (temperatura * 9 / 5) + 32
                print(f"Risultato: {risultato:.2f} F")
            else:
                print("L'unità di partenza deve essere Celsius")

        case "2":
            if unita == "F":
                risultato = (temperatura - 32) * 5 / 9
                print(f"Risultato: {risultato:.2f} C")
            else:
                print("L'unità di partenza deve essere Fahrenheit")

        case "3":
            if unita == "C":
                risultato = temperatura + 273.15
                print(f"Risultato: {risultato:.2f} K")
            else:
                print("L'unità di partenza deve essere Celsius")

        case "4":
            if unita == "K":
                risultato = temperatura - 273.15
                print(f"Risultato: {risultato:.2f} C")
            else:
                print("L'unità di partenza deve essere Kelvin")

        case "5":
            print("Chiusura del menu")
            break

        case _:
            print("Scelta non valida")

# ---------------------------------------------------------
# 2. Analizzatore di una frase

# Chiedere all'utente una frase e calcolare:

#     numero totale di caratteri;
#     numero di caratteri esclusi gli spazi;
#     numero di parole;
#     numero di vocali e consonanti;
#     numero di cifre;
#     prima e ultima parola.

# Ignorare maiuscole e minuscole e gestire il caso di stringa vuota.
# ---------------------------------------------------------

"""
An outer while loop handles the menu with match; an inner loop asks for
the sentence and rejects empty input after strip().
 
Characters and words are counted with len(), replace() and split().
Vowels, consonants and digits are counted character by character with
isalpha() and isdigit(), so spaces and punctuation are ignored. The first
and last word come from the list returned by split().
"""
while True:
    frase = input("Inserisci una frase: ").strip()

    if not frase:
        print("La frase non può essere vuota. Riprovare: ")
        continue
    break

while True:
    print("\n--- Menu ---")
    print("1. Numero totale di caratteri")
    print("2. Numero di caratteri esclusi gli spazi")
    print("3. Numero di parole")
    print("4. Numero di vocali e consonanti")
    print("5. Numero di cifre")
    print("6. Prima e ultima parola")
    print("7. Uscire")

    scelta = input("Scelta: ")

    match scelta:
        case "1":
            print(f"Numero totale di caratteri: {len(frase)}")

        case "2":
            print(
                f"Numero di caratteri esclusi gli spazi: {len(frase.replace(' ', ''))}"
            )

        case "3":
            print(f"Numero di parole: {len(frase.split())}")

        case "4":
            vocali = "aeiou"
            numero_vocali = 0
            numero_consonanti = 0

            # controllo ogni carattere per distinguere vocali e consonanti
            for carattere in frase.lower():
                if carattere in vocali:
                    numero_vocali += 1
                elif carattere.isalpha():
                    numero_consonanti += 1

            print(
                f"Numero di vocali: {numero_vocali} e consonanti: {numero_consonanti}"
            )

        case "5":
            numero_cifre = 0

            for carattere in frase:
                if carattere.isdigit():
                    numero_cifre += 1
            print(f"Numero di cifre: {numero_cifre}")

        case "6":
            parole = frase.split()
            print(f"Prima parola: {parole[0]} e ultima: {parole[-1]}")

        case "7":
            print("Chiusura del menu")
            break

        case _:
            print("Scelta non valida")

# ---------------------------------------------------------
# 3. Registro delle temperature

# Dichiarare o costruire una lista contenente le temperature di una settimana e calcolare:

#     temperatura minima e massima;
#     temperatura media;
#     numero di giorni sopra la media;
#     numero di giorni sotto o uguali alla media;
#     variazione tra primo e ultimo giorno;
#     elenco delle temperature positive e negative.

# Non utilizzare inizialmente min, max e sum: calcolare i valori con cicli.
# ---------------------------------------------------------

"""
The first loop computes minimum, maximum and total sum in a single pass
and splits the values into the positive and negative lists.
 
The average needs the total sum, so it is computed after that loop and a
second loop is required to count the days above and below/equal to it.
The variation is the difference between the last and the first element.
"""
temperature = [-1, 30, 32, 15, -3, 25, 30]
temperatura_minima = temperature[0]
temperatura_massima = temperature[0]
somma = 0
giorni_sopra_media = 0
giorni_sotto_uguali_media = 0
positive = []
negative = []

print(f"Lista temperature: {temperature}")

for temperatura in temperature:

    if temperatura < temperatura_minima:
        temperatura_minima = temperatura

    if temperatura > temperatura_massima:
        temperatura_massima = temperatura

    somma += temperatura

    if temperatura > 0:
        positive.append(temperatura)
    elif temperatura < 0:
        negative.append(temperatura)

media = somma / len(temperature)

for temperatura in temperature:

    if temperatura > media:
        giorni_sopra_media += 1
    else:
        giorni_sotto_uguali_media += 1

variazione = temperature[-1] - temperature[0]

print(f"Temperatura minima: {temperatura_minima}")
print(f"Temperatura massima: {temperatura_massima}")
print(f"Temperatura media: {media:.2f}")
print(f"Giorni sopra la media: {giorni_sopra_media}")
print(f"Giorni sotto o uguali alla media: {giorni_sotto_uguali_media}")
print(f"Variazione primo/ultimo giorno: {variazione}")
print(f"Temperature positive: {positive}")
print(f"Temperature negative: {negative}")

# ---------------------------------------------------------
# 4. Cassa automatica

# Simulare una cassa chiedendo ripetutamente il prezzo degli articoli.
# L'inserimento termina quando l'utente digita 0.

# Mostrare totale, numero di articoli, prezzo medio, articolo più costoso ed eventuale sconto:

#     meno di 50 euro: nessuno sconto;
#     da 50 a 99.99 euro: 5%;
#     da 100 a 199.99 euro: 10%;
#     almeno 200 euro: 15%.

# Gestire prezzi negativi senza interrompere il programma.
# ---------------------------------------------------------

"""
Input loop: try/except rejects non numeric prices, negative prices are
refused with continue without stopping the program, and 0 ends the input.
 
Total, number of items and highest price are updated inside the loop, so
no list of items is needed. If at least one item was entered, the program
then computes the average, the discount band and the final price.
"""
totale = 0
numero_articoli = 0
articolo_piu_costoso = 0

while True:
    try:
        prezzo = float(input("Inserisci il prezzo dell'articolo (0 per terminare): "))

        if prezzo == 0:
            break

        if prezzo < 0:
            print("Il prezzo non può essere negativo. Riprova")
            continue

        totale += prezzo
        numero_articoli += 1

        # aggiorno il prezzo più alto trovato
        if prezzo > articolo_piu_costoso:
            articolo_piu_costoso = prezzo

    except ValueError:
        print("Inserisci un prezzo valido")

if numero_articoli > 0:
    prezzo_medio = totale / numero_articoli

    if totale < 50:
        sconto = 0
    elif totale < 100:
        sconto = 5
    elif totale < 200:
        sconto = 10
    else:
        sconto = 15

    importo_sconto = totale * sconto / 100
    totale_finale = totale - importo_sconto

    print("\n--- Riepilogo ---")
    print(f"Totale: {totale:.2f} €")
    print(f"Numero di articoli: {numero_articoli}")
    print(f"Prezzo medio: {prezzo_medio:.2f} €")
    print(f"Articolo più costoso: {articolo_piu_costoso:.2f} €")
    print(f"Sconto: {sconto}%")
    print(f"Totale finale: {totale_finale:.2f} €")
else:
    print("Nessun articolo inserito.")

# ---------------------------------------------------------
# 5. Tabellone dei punteggi

# Dati i punteggi di una classe, calcolare media, minimo, massimo, insufficienze,
# voti almeno pari a 8 e lista dei voti sufficienti.

# Mostrare inoltre i voti ordinati e il voto più frequente, se presente.
# Distinguere tra voti non validi, insufficienze e sufficienze.
# ---------------------------------------------------------

"""
First loop: grades outside the 0-10 range are reported and skipped with
continue. Valid ones are stored and used to update sum, minimum, maximum,
insufficient grades, grades >= 8 and the list of sufficient grades.
Minimum and maximum start at None because the first grade may be invalid.
 
Second part: average over the valid grades only, sorted() for the ranking
and a frequency dictionary scanned by a loop that keeps the highest count.
The most frequent grade is shown only if its frequency is greater than 1.
"""
voti = [7, 8, 5, 10, 6, 8, 4, 9, 11, -2, 8, 3]
somma = 0
minimo = None
massimo = None
insufficienze = 0
voti_almeno_8 = 0
voti_sufficienti = []
voti_validi = []

for voto in voti:

    if voto < 0 or voto > 10:
        print(f"Voto non valido: {voto}")
        continue

    voti_validi.append(voto)
    somma += voto

    if minimo is None or voto < minimo:
        minimo = voto

    if massimo is None or voto > massimo:
        massimo = voto

    if voto < 6:
        insufficienze += 1
    else:
        voti_sufficienti.append(voto)

    if voto >= 8:
        voti_almeno_8 += 1

if voti_validi:
    media = somma / len(voti_validi)
    voti_ordinati = sorted(voti_validi)
    frequenze = {}
    for voto in voti_validi:
        if voto not in frequenze:
            frequenze[voto] = 1
        else:
            frequenze[voto] += 1

    frequenza_massima = 0
    voto_piu_frequente = None

    for voto, frequenza in frequenze.items():
        if frequenza > frequenza_massima:
            frequenza_massima = frequenza
            voto_piu_frequente = voto

    print("\n--- Tabellone dei punteggi ---")
    print(f"Lista voti: {voti}")
    print(f"Media: {media:.2f}")
    print(f"Minimo: {minimo}")
    print(f"Massimo: {massimo}")
    print(f"Insufficienze: {insufficienze}")
    print(f"Voti almeno pari a 8: {voti_almeno_8}")
    print(f"Voti sufficienti: {voti_sufficienti}")
    print(f"Voti ordinati: {voti_ordinati}")

    if frequenza_massima > 1:
        print(f"Voto più frequente: {voto_piu_frequente}")
    else:
        print("Non c'è un voto più frequente")

else:
    print("Non ci sono voti validi")

# ---------------------------------------------------------
# 6. Codificatore di testo

# Trasformare una frase sostituendo ogni vocale con il carattere successivo nell'alfabeto.
# Consonanti, spazi e punteggiatura devono rimanere invariati.
#
# Realizzare anche una modalità di decodifica che ricostruisca il testo originale.
#
# Nota: viene utilizzato il carattere # come marcatore per rendere
# la codifica completamente reversibile.
#
# Esempio:
# Input: casa
# Output: c#bs#b
# ---------------------------------------------------------

"""
The encoding map replaces each vowel with "#" plus the next letter of the
alphabet; the decoding map is simply the reverse of it.
 
Encoding works character by character and keeps the original case.
Decoding instead uses an index, because every encoded vowel takes two
characters: it reads "#" plus the following letter and, on a match,
moves the index forward by two positions.
 
Case 4 is a placeholder for a future custom shift.
"""
alfabeto = "abcdefghijklmnopqrstuvwxyz"
vocali = "aeiou"

codifica = {}
for vocale in vocali:
    posizione = alfabeto.index(vocale)
    codifica[vocale] = "#" + alfabeto[posizione + 1]

decodifica = {}
for vocale, sostituto in codifica.items():
    decodifica[sostituto] = vocale


def codifica_frase(frase):
    frase_codificata = ""
    for carattere in frase:
        minuscolo = carattere.lower()
        if minuscolo in codifica:
            nuovo_carattere = codifica[minuscolo]
            if carattere.isupper():
                nuovo_carattere = nuovo_carattere.upper()
            frase_codificata += nuovo_carattere
        else:
            frase_codificata += carattere
    return frase_codificata


def decodifica_frase(frase):
    frase_decodificata = ""
    i = 0
    while i < len(frase):
        if frase[i] == "#" and i + 1 < len(frase):
            codice = frase[i : i + 2].lower()
            if codice in decodifica:
                nuovo_carattere = decodifica[codice]
                if frase[i + 1].isupper():
                    nuovo_carattere = nuovo_carattere.upper()
                frase_decodificata += nuovo_carattere
                i += 2
                continue
        frase_decodificata += frase[i]
        i += 1
    return frase_decodificata


# La frase viene chiesta UNA SOLA VOLTA
frase = input("Inserisci una frase: ")

while True:
    print("\n--- Menu ---")
    print("1. Codificare la frase")
    print("2. Decodificare la frase")
    print("3. Uscire")

    scelta = input("Scegli un'opzione: ")

    match scelta:
        case "1":
            print(f"Testo codificato: {codifica_frase(frase)}")

        case "2":
            print(f"Testo decodificato: {decodifica_frase(frase)}")

        case "3":
            print("Chiusura del programma")
            break

        case _:
            print("Scelta non valida")

# ---------------------------------------------------------
# 7. Rimozione dei duplicati mantenendo l'ordine

# Data una lista con valori ripetuti, costruire una nuova lista senza duplicati, mantenendo la prima occorrenza.

# valori = [4, 2, 4, 7, 2, 9, 7, 1]
# # Risultato: [4, 2, 7, 9, 1]

# Svolgere l'esercizio in due versioni: usando una lista di controllo e usando un set.
# ---------------------------------------------------------

"""
Due versioni dello stesso esercizio. La prima usa una lista di controllo
e verifica l'appartenenza con "not in"; la seconda usa un set, che non
puo' contenere duplicati e rende il controllo piu' veloce.
 
In entrambi i casi il risultato viene tenuto in una lista, cosi' da
preservare l'ordine originale delle prime occorrenze.
"""
valori = [4, 2, 4, 7, 2, 9, 7, 1]
risultato_list = []
controllo_list = []
risultato_set = []
controllo_set = set()

print(f"Lista: {valori}")

for valore in valori:
    if valore not in controllo_list:
        controllo_list.append(valore)
        risultato_list.append(valore)

print(f"Risultato list(): {risultato_list}")

for valore in valori:
    if valore not in controllo_set:
        controllo_set.add(valore)
        risultato_set.append(valore)

print(f"Risultato set(): {risultato_set}")

# ---------------------------------------------------------
# 8. Frequenza delle parole

# Chiedere un testo e costruire un dizionario in cui ogni chiave sia
# una parola e ogni valore il numero di occorrenze.

# Ignorare maiuscole e minuscole, rimuovere la punteggiatura, mostrare la parola più frequente,
# le parole presenti una sola volta e le parole in ordine alfabetico.

# Input: Python è semplice e Python è potente
# python: 2
# è: 2
# semplice: 1
# e: 1
# potente: 1
# ---------------------------------------------------------

"""
The text is lowercased and stripped of punctuation before split(), so the
same word written differently is counted only once. A dictionary stores
each word with its number of occurrences.
 
Separate loops then handle each analysis: the most frequent word (keeping
the highest frequency found so far), the words appearing only once, and
the alphabetical listing obtained with sorted() on the keys, which leaves
the original dictionary unchanged.
"""
testo = input("Inserisci un testo: ").lower()

for carattere in ".,;:!?":
    testo = testo.replace(carattere, "")

parole = testo.split()
frequenze = {}

for parola in parole:
    if parola in frequenze:
        frequenze[parola] += 1
    else:
        frequenze[parola] = 1

print("\n--- Frequenza delle parole ---")
for parola, frequenza in frequenze.items():
    print(f"{parola}: {frequenza}")

print("\n--- Parola più frequente ---")

parola_piu_frequente = None
frequenza_massima = 0

for parola, frequenza in frequenze.items():
    if frequenza > frequenza_massima:
        parola_piu_frequente = parola
        frequenza_massima = frequenza

print(f"{parola_piu_frequente}: {frequenza_massima}")

print("\n--- Parole presenti una sola volta ---")

for parola, frequenza in frequenze.items():
    if frequenza == 1:
        print(parola)

print("\n--- Parole in ordine alfabetico ---")

for parola in sorted(frequenze):
    print(f"{parola}: {frequenze[parola]}")

# ---------------------------------------------------------
# 9. Rubrica telefonica

# Costruire una rubrica con un dizionario. Ogni contatto deve avere nome, numero di telefono e categoria.

# Creare un menu con le operazioni:

#     aggiungere un contatto;
#     cercare un contatto;
#     modificare un numero;
#     eliminare un contatto;
#     mostrare tutti i contatti;
#     mostrare i contatti di una categoria;
#     uscire.

# Gestire i casi di contatto inesistente.
# ---------------------------------------------------------

"""
Contacts are stored in a dictionary: the name is the key, number and
category are kept together in a nested dictionary. A while loop with match
handles the menu.
 
Adding asks for confirmation when the name already exists, so a contact is
not overwritten by mistake. Search, edit and delete first check that the
name is in the dictionary. The category filter compares in lowercase and
uses the flag trovati to report when nothing matches.
 
Option 7 (file export) is left as a TODO.
"""
rubrica = {}

while True:
    print("\n--- Rubrica ---")
    print("1. Aggiungere un contatto")
    print("2. Cercare un contatto")
    print("3. Modificare un numero")
    print("4. Eliminare un contatto")
    print("5. Mostrare tutti i contatti")
    print("6. Mostrare i contatti di una categoria")
    print("7. Esportare la rubrica su file")
    print("8. Uscire")

    scelta = input("Scegli un'opzione: ")

    match scelta:

        case "1":
            nome = input("Nome: ")

            if nome in rubrica:
                conferma = input(
                    f"Il contatto '{nome}' esiste già. Vuoi sovrascriverlo? (s/n): "
                ).lower()

                if conferma != "s":
                    print("Operazione annullata.")
                    continue

            numero = input("Numero di telefono: ")

            print("Scegli una categoria:")
            print("1. Famiglia")
            print("2. Amici")
            print("3. Lavoro")
            print("4. Altro")

            scelta_categoria = input("Scelta: ")

            match scelta_categoria:
                case "1":
                    categoria = "Famiglia"
                case "2":
                    categoria = "Amici"
                case "3":
                    categoria = "Lavoro"
                case "4":
                    categoria = "Altro"
                case _:
                    print("Categoria non valida")
                    continue

            rubrica[nome] = {"numero": numero, "categoria": categoria}

            print("Contatto aggiunto")

        case "2":
            nome = input("Nome del contatto: ")

            if nome in rubrica:
                print(f"Nome: {nome}")
                print(f"Numero: {rubrica[nome]['numero']}")
                print(f"Categoria: {rubrica[nome]['categoria']}")
            else:
                print("Contatto inesistente")

        case "3":
            nome = input("Nome del contatto: ")

            if nome in rubrica:
                nuovo_numero = input("Nuovo numero: ")
                rubrica[nome]["numero"] = nuovo_numero
                print("Numero modificato")
            else:
                print("Contatto inesistente")

        case "4":
            nome = input("Nome del contatto: ")

            if nome in rubrica:
                del rubrica[nome]
                print("Contatto eliminato")
            else:
                print("Contatto inesistente")

        case "5":
            if rubrica:
                for nome, dati in rubrica.items():
                    print(f"{nome} - " f"{dati['numero']} - " f"{dati['categoria']}")
            else:
                print("La rubrica è vuota")

        case "6":
            categoria = input("Categoria: ")

            trovati = False

            for nome, dati in rubrica.items():
                if dati["categoria"].lower() == categoria.lower():
                    print(f"{nome} - {dati['numero']}")
                    trovati = True

            if not trovati:
                print("Nessun contatto trovato")

        case "7":
            # TODO: esportazione della rubrica su file
            pass

        case "8":
            print("Chiusura della rubrica")
            break

        case _:
            print("Scelta non valida")

# ---------------------------------------------------------
# 10. Statistiche sulle parole

# Dato un testo, costruire un dizionario associando a ogni parola:

#     lunghezza;
#     numero di vocali;
#     numero di consonanti;
#     numero di occorrenze.

# {
#     "python": {
#         "lunghezza": 6,
#         "vocali": 1,
#         "consonanti": 5,
#         "occorrenze": 2
#     }
# }

# Mostrare la parola più lunga, quella con più vocali, quella più frequente,
# la lunghezza media e le parole sopra la media.
# ---------------------------------------------------------

"""
The text is lowercased, cleaned of punctuation and split into words.
The dictionary statistiche stores length, vowels, consonants and
occurrences: the values are computed the first time a word appears, later
only the counter is increased. Consonants count only alphabetic characters
that are not vowels.
 
Separate loops find the longest word, the one with most vowels and the
most frequent one. The average length is computed over all the words,
repetitions included, and is then used to build the list of words above it.
The analyses run only if the dictionary is not empty.
"""
testo = input("Inserisci un testo: ").lower()

for carattere in ".,;:!?":
    testo = testo.replace(carattere, "")

parole = testo.split()
statistiche = {}

for parola in parole:

    if parola not in statistiche:
        vocali = 0
        consonanti = 0

        for carattere in parola:
            if carattere in "aeiou":
                vocali += 1
            elif carattere.isalpha():
                consonanti += 1

        statistiche[parola] = {
            "lunghezza": len(parola),
            "vocali": vocali,
            "consonanti": consonanti,
            "occorrenze": 1,
        }

    else:
        statistiche[parola]["occorrenze"] += 1


if statistiche:
    parola_piu_lunga = None
    lunghezza_massima = 0

    for parola, dati in statistiche.items():
        if dati["lunghezza"] > lunghezza_massima:
            lunghezza_massima = dati["lunghezza"]
            parola_piu_lunga = parola

    parola_piu_vocali = None
    numero_vocali_massimo = 0

    for parola, dati in statistiche.items():
        if dati["vocali"] > numero_vocali_massimo:
            numero_vocali_massimo = dati["vocali"]
            parola_piu_vocali = parola

    parola_piu_frequente = None
    frequenza_massima = 0

    for parola, dati in statistiche.items():
        if dati["occorrenze"] > frequenza_massima:
            frequenza_massima = dati["occorrenze"]
            parola_piu_frequente = parola

    somma_lunghezze = 0

    for parola in parole:
        somma_lunghezze += len(parola)

    lunghezza_media = somma_lunghezze / len(parole)
    parole_sopra_media = []

    for parola, dati in statistiche.items():
        if dati["lunghezza"] > lunghezza_media:
            parole_sopra_media.append(parola)

    print("\n--- Statistiche sulle parole ---")
    for parola, dati in statistiche.items():
        print(f"{parola}: {dati}")

    print(f"\nParola più lunga: {parola_piu_lunga} ({lunghezza_massima} caratteri)")
    print(
        f"Parola con più vocali: {parola_piu_vocali} ({numero_vocali_massimo} vocali)"
    )
    print(f"Parola più frequente: {parola_piu_frequente} ({frequenza_massima} volte)")
    print(f"Lunghezza media: {lunghezza_media:.2f}")
    print(f"Parole sopra la media: {parole_sopra_media}")

else:
    print("Nessuna parola inserita")

# ---------------------------------------------------------
# 11. Sistema di prenotazione dei posti

# Simulare la gestione dei posti di una sala con 5 file e 8 posti per fila,
# usando una lista di liste.
#
# Consentire di visualizzare la sala, prenotare e annullare un posto,
# contare posti liberi e occupati e verificare se una fila è completa.
#
# Impedire prenotazioni di posti già occupati o inesistenti.
#
# Fila 1: O O X O O O O O
# Fila 2: O X O O O O O O
# ---------------------------------------------------------

"""
The room is a list of lists, with "O" for a free seat and "X" for an
occupied one. A while loop with match handles the menu.
 
Row and seat are entered starting from 1, so 1 is subtracted before
indexing the list; range checks and try/except prevent invalid access.
Counting free and occupied seats needs two nested loops, and a row is
considered full when "O" is no longer in it.
"""
sala = [
    ["O", "O", "O", "O", "O", "O", "O", "O"],
    ["O", "O", "O", "O", "O", "O", "O", "O"],
    ["O", "O", "O", "O", "O", "O", "O", "O"],
    ["O", "O", "O", "O", "O", "O", "O", "O"],
    ["O", "O", "O", "O", "O", "O", "O", "O"],
]

while True:
    print("\n--- Sistema di prenotazione ---")
    print("1. Visualizzare la sala")
    print("2. Prenotare un posto")
    print("3. Annullare un posto")
    print("4. Contare posti liberi e occupati")
    print("5. Verificare se una fila è completa")
    print("6. Uscire")

    scelta = input("Scegli un'opzione: ")

    match scelta:

        case "1":
            print("\n--- Sala ---")

            for indice, fila in enumerate(sala, start=1):
                print(f"Fila {indice}: {' '.join(fila)}")

        case "2":
            try:
                fila = int(input("Inserisci il numero della fila (1-5): "))
                posto = int(input("Inserisci il numero del posto (1-8): "))

                if fila < 1 or fila > 5 or posto < 1 or posto > 8:
                    print("Fila o posto inesistente")
                    continue

                if sala[fila - 1][posto - 1] == "X":
                    print("Il posto è già occupato")
                else:
                    sala[fila - 1][posto - 1] = "X"
                    print("Posto prenotato.")

            except ValueError:
                print("Inserisci dei numeri validi")

        case "3":
            try:
                fila = int(input("Inserisci il numero della fila (1-5): "))
                posto = int(input("Inserisci il numero del posto (1-8): "))

                if fila < 1 or fila > 5 or posto < 1 or posto > 8:
                    print("Fila o posto inesistente")
                    continue

                if sala[fila - 1][posto - 1] == "O":
                    print("Il posto è già libero")
                else:
                    sala[fila - 1][posto - 1] = "O"
                    print("Prenotazione annullata")

            except ValueError:
                print("Inserisci dei numeri validi")

        case "4":
            posti_liberi = 0
            posti_occupati = 0

            for fila in sala:
                for posto in fila:
                    if posto == "O":
                        posti_liberi += 1
                    else:
                        posti_occupati += 1

            print(f"Posti liberi: {posti_liberi}")
            print(f"Posti occupati: {posti_occupati}")

        case "5":
            try:
                fila = int(input("Inserisci il numero della fila (1-5): "))

                if fila < 1 or fila > 5:
                    print("Fila inesistente.")
                    continue

                if "O" not in sala[fila - 1]:
                    print(f"La fila {fila} è completa")
                else:
                    print(f"La fila {fila} non è completa")

            except ValueError:
                print("Inserisci un numero valido")

        case "6":
            print("Chiusura del programma")
            break

        case _:
            print("Scelta non valida")

# ---------------------------------------------------------
# 12. Inventario di un magazzino

# Creare un inventario con un dizionario. Per ogni prodotto memorizzare quantità, prezzo e categoria.

# Il programma deve permettere di inserire prodotti, modificare quantità,
# registrare vendite, calcolare il valore totale, mostrare prodotti sotto scorta,
# trovare il prodotto più costoso, filtrare per categoria ed eliminare prodotti.

# Una vendita non deve essere accettata se la quantità richiesta supera quella disponibile.
# Concetti: dizionari annidati, condizioni, aggiornamento dati, cicli.
# ---------------------------------------------------------

"""
Products are stored in a dictionary: the name is the key, quantity, price
and category are kept in a nested dictionary. A while loop with match
handles the menu.
 
Insert and edit reject negative values and use try/except on the numbers.
A sale is accepted only if the quantity is positive and not greater than
the stock. The total value is the sum of quantity * price.
 
Low stock and the category filter use a threshold and the flag trovati to
report when nothing matches; the most expensive product is found by
comparing the prices one by one.
"""
inventario = {}

while True:
    print("\n--- Inventario ---")
    print("1. Inserire un prodotto")
    print("2. Modificare quantità")
    print("3. Registrare una vendita")
    print("4. Calcolare il valore totale")
    print("5. Mostrare prodotti sotto scorta")
    print("6. Trovare il prodotto più costoso")
    print("7. Filtrare per categoria")
    print("8. Eliminare un prodotto")
    print("9. Uscire")

    scelta = input("Scegli un'opzione: ")

    match scelta:

        case "1":
            nome = input("Nome del prodotto: ")

            if nome in inventario:
                print("Il prodotto esiste già")
            else:
                try:
                    quantita = int(input("Quantità: "))
                    prezzo = float(input("Prezzo: "))

                    print("Scegli una categoria:")
                    print("1. Alimentari")
                    print("2. Elettronica")
                    print("3. Abbigliamento")
                    print("4. Casa")

                    scelta_categoria = input("Scelta: ")

                    match scelta_categoria:
                        case "1":
                            categoria = "Alimentari"
                        case "2":
                            categoria = "Elettronica"
                        case "3":
                            categoria = "Abbigliamento"
                        case "4":
                            categoria = "Casa"
                        case _:
                            print("Categoria non valida")
                            continue

                    if quantita < 0 or prezzo < 0:
                        print("Quantità e prezzo non possono essere negativi")
                    else:
                        inventario[nome] = {
                            "quantita": quantita,
                            "prezzo": prezzo,
                            "categoria": categoria,
                        }

                        print("Prodotto inserito.")

                except ValueError:
                    print("Inserisci una quantità e un prezzo validi")

        case "2":
            ricerca = input("Cerca il prodotto: ").lower()

            prodotti_trovati = []

            for nome in inventario:
                if ricerca in nome.lower():
                    prodotti_trovati.append(nome)

            if not prodotti_trovati:
                print("Nessun prodotto trovato")
                continue

            print("\n--- Prodotti trovati ---")

            for i, nome in enumerate(prodotti_trovati, start=1):
                print(f"{i}. {nome}")

            try:
                scelta_prodotto = int(input("Scegli il prodotto: "))

                if scelta_prodotto < 1 or scelta_prodotto > len(prodotti_trovati):
                    print("Scelta non valida.")
                    continue

                nome = prodotti_trovati[scelta_prodotto - 1]

                nuova_quantita = int(input("Nuova quantità: "))

                if nuova_quantita < 0:
                    print("La quantità non può essere negativa")
                else:
                    inventario[nome]["quantita"] = nuova_quantita
                    print("Quantità modificata.")

            except ValueError:
                print("Inserisci un numero valido")

        case "3":
            ricerca = input("Cerca il prodotto: ").lower()

            prodotti_trovati = []

            for nome in inventario:
                if ricerca in nome.lower():
                    prodotti_trovati.append(nome)

            if not prodotti_trovati:
                print("Nessun prodotto trovato")
                continue

            print("\n--- Prodotti trovati ---")

            for i, nome in enumerate(prodotti_trovati, start=1):
                print(f"{i}. {nome}")

            try:
                scelta_prodotto = int(input("Scegli il prodotto: "))

                if scelta_prodotto < 1 or scelta_prodotto > len(prodotti_trovati):
                    print("Scelta non valida.")
                    continue

                nome = prodotti_trovati[scelta_prodotto - 1]

                quantita_venduta = int(input("Quantità da vendere: "))

                if quantita_venduta <= 0:
                    print("La quantità deve essere maggiore di zero")

                elif quantita_venduta > inventario[nome]["quantita"]:
                    print("Quantità richiesta superiore a quella disponibile")

                else:
                    inventario[nome]["quantita"] -= quantita_venduta
                    print("Vendita registrata")

            except ValueError:
                print("Inserisci un numero valido")

        case "4":
            valore_totale = 0

            for nome, dati in inventario.items():
                valore_totale += dati["quantita"] * dati["prezzo"]

            print(f"Valore totale dell'inventario: {valore_totale:.2f} €")

        case "5":
            soglia = 5
            trovati = False

            print("\n--- Prodotti sotto scorta ---")

            for nome, dati in inventario.items():
                if dati["quantita"] < soglia:
                    print(f"{nome}: {dati['quantita']} pezzi")
                    trovati = True

            if not trovati:
                print("Nessun prodotto sotto scorta")

        case "6":
            if inventario:
                prodotto_piu_costoso = None

                for nome, dati in inventario.items():
                    if prodotto_piu_costoso is None:
                        prodotto_piu_costoso = nome
                    elif dati["prezzo"] > inventario[prodotto_piu_costoso]["prezzo"]:
                        prodotto_piu_costoso = nome

                print(
                    f"Prodotto più costoso: {prodotto_piu_costoso} - "
                    f"{inventario[prodotto_piu_costoso]['prezzo']:.2f} €"
                )

            else:
                print("L'inventario è vuoto")

        case "7":
            ricerca = input("Cerca la categoria: ").lower()

            prodotti_trovati = []

            for nome, dati in inventario.items():
                if ricerca in dati["categoria"].lower():
                    prodotti_trovati.append(nome)

            if not prodotti_trovati:
                print("Nessun prodotto trovato")
                continue

            print("\n--- Prodotti trovati ---")

            for nome in prodotti_trovati:
                dati = inventario[nome]
                print(
                    f"{nome} - "
                    f"Categoria: {dati['categoria']} - "
                    f"Quantità: {dati['quantita']} - "
                    f"Prezzo: {dati['prezzo']:.2f} €"
                )

        case "8":
            ricerca = input("Cerca il prodotto da eliminare: ").lower()

            prodotti_trovati = []

            for nome in inventario:
                if ricerca in nome.lower():
                    prodotti_trovati.append(nome)

            if not prodotti_trovati:
                print("Nessun prodotto trovato")
                continue

            print("\n--- Prodotti trovati ---")

            for i, nome in enumerate(prodotti_trovati, start=1):
                print(f"{i}. {nome}")

            try:
                scelta_prodotto = int(input("Scegli il prodotto: "))

                if scelta_prodotto < 1 or scelta_prodotto > len(prodotti_trovati):
                    print("Scelta non valida")
                    continue

                nome = prodotti_trovati[scelta_prodotto - 1]

                del inventario[nome]
                print("Prodotto eliminato")

            except ValueError:
                print("Inserisci un numero valido")

        case "9":
            print("Chiusura dell'inventario")
            break

        case _:
            print("Scelta non valida")

# ---------------------------------------------------------
# 13. Analisi dei voti per studente

# Dati gli studenti e i voti di più materie, costruire una struttura di dizionari annidati.

# studenti = {
#     "Anna": {
#         "matematica": 8,
#         "informatica": 9,
#         "inglese": 7
#     },
#     "Luca": {
#         "matematica": 5,
#         "informatica": 6,
#         "inglese": 7
#     }
# }

# Calcolare la media di ogni studente e della classe per materia, trovare i migliori,
# individuare gli insufficienti e ordinare gli studenti per media decrescente.
# ---------------------------------------------------------

"""
Nested dictionaries: one dictionary of grades per student.
 
The average of each student is computed first and stored in a separate
dictionary so it can be reused by the following analyses. The class
average per subject takes the subjects from the first student and sums
the grades of everybody.
 
The best students are kept in a list to handle ties, and a flag reports
when there are no insufficient grades. The final ranking uses sorted()
with key=lambda on the average (second element of each pair) and
reverse=True, leaving the original dictionary unchanged.
"""
studenti = {
    "Anna": {"matematica": 8, "informatica": 9, "inglese": 7},
    "Luca": {"matematica": 5, "informatica": 6, "inglese": 7},
    "Marco": {"matematica": 9, "informatica": 8, "inglese": 9},
    "Sara": {"matematica": 6, "informatica": 5, "inglese": 6},
}

medie_studenti = {}

print(f"Voti degli studenti: \n{json.dumps(studenti, indent=4)}")

for nome, voti in studenti.items():
    somma = 0

    for voto in voti.values():
        somma += voto

    media = somma / len(voti)
    medie_studenti[nome] = media

print("\n--- Media di ogni studente ---")

for nome, media in medie_studenti.items():
    print(f"{nome}: {media:.2f}")

medie_materie = {}

materie = list(studenti["Anna"].keys())

for materia in materie:
    somma = 0

    for voti in studenti.values():
        somma += voti[materia]

    media = somma / len(studenti)
    medie_materie[materia] = media

print("\n--- Media della classe per materia ---")

for materia, media in medie_materie.items():
    print(f"{materia}: {media:.2f}")

media_massima = None
migliori = []

for nome, media in medie_studenti.items():

    if media_massima is None or media > media_massima:
        media_massima = media
        migliori = [nome]

    elif media == media_massima:
        migliori.append(nome)

print("\n--- Studenti con la media più alta ---")

for nome in migliori:
    print(f"{nome}: {medie_studenti[nome]:.2f}")

print("\n--- Studenti con insufficienze ---")

trovati = False

for nome, voti in studenti.items():

    for materia, voto in voti.items():

        if voto < 6:
            print(f"{nome}: {materia} = {voto}")
            trovati = True

if not trovati:
    print("Non ci sono insufficienze")

studenti_ordinati = sorted(
    medie_studenti.items(), key=lambda elemento: elemento[1], reverse=True
)

print("\n--- Studenti ordinati per media ---")

for nome, media in studenti_ordinati:
    print(f"{nome}: {media:.2f}")


# ---------------------------------------------------------
# 14. Gioco del labirinto testuale

# Creare un gioco ambientato in una griglia rappresentata da una lista di liste.

# labirinto = [
#     ["#", "#", "#", "#", "#", "#"],
#     ["#", "P", " ", " ", "T", "#"],
#     ["#", "#", " ", "#", " ", "#"],
#     ["#", " ", " ", "#", " ", "#"],
#     ["#", "#", "#", "#", "#", "#"]
# ]

# Il giocatore si muove con w, a, s, d.
# Impedire il passaggio sui muri e l'uscita dalla griglia,
# contare le mosse, terminare al raggiungimento del tesoro e gestire q per uscire.
# ---------------------------------------------------------

"""
The maze is a list of lists: "#" walls, " " free space, "P" the player and
"T" the treasure. Row and column are kept in separate variables.
 
For every command the program first builds nuova_riga and nuova_colonna,
then checks that the destination is inside the grid and is not a wall
before moving the player.
 
The content of the destination is saved before writing "P": that is how
the treasure is detected. After a valid move the old cell is cleared and
the counter increased; finding "T" ends the loop.
"""
labirinto = [
    ["#", "#", "#", "#", "#", "#"],
    ["#", "P", " ", " ", "T", "#"],
    ["#", "#", " ", "#", " ", "#"],
    ["#", " ", " ", "#", " ", "#"],
    ["#", "#", "#", "#", "#", "#"],
]

riga = 1
colonna = 1
mosse = 0

while True:
    print("\n--- Labirinto ---")

    for riga_labirinto in labirinto:
        print(" ".join(riga_labirinto))

    print("\nComandi: w = su, a = sinistra, s = giù, d = destra, q = uscire")
    comando = input("Scegli una direzione: ").lower()

    if comando == "q":
        print("Hai abbandonato il labirinto")
        break

    nuova_riga = riga
    nuova_colonna = colonna

    if comando == "w":
        nuova_riga -= 1

    elif comando == "s":
        nuova_riga += 1

    elif comando == "a":
        nuova_colonna -= 1

    elif comando == "d":
        nuova_colonna += 1

    else:
        print("Comando non valido.")
        continue

    if (
        nuova_riga < 0
        or nuova_riga >= len(labirinto)
        or nuova_colonna < 0
        or nuova_colonna >= len(labirinto[0])
    ):
        print("Non puoi uscire dalla griglia.")
        continue

    if labirinto[nuova_riga][nuova_colonna] == "#":
        print("Non puoi attraversare un muro.")
        continue

    destinazione = labirinto[nuova_riga][nuova_colonna]
    labirinto[riga][colonna] = " "
    riga = nuova_riga
    colonna = nuova_colonna
    labirinto[riga][colonna] = "P"
    mosse += 1

    if destinazione == "T":
        print("\nHai trovato il tesoro!")
        print(f"Hai completato il labirinto in {mosse} mosse")
        break

# ---------------------------------------------------------
# 15. Simulatore di portafoglio digitale

# Realizzare un programma che simuli un portafoglio digitale.
# Ogni transazione deve contenere tipo, importo, categoria e descrizione.

# {
#     "tipo": "uscita",
#     "importo": 24.50,
#     "categoria": "trasporti",
#     "descrizione": "Abbonamento bus"
# }

# Il menu deve permettere di:

#     registrare un'entrata;
#     registrare un'uscita;
#     visualizzare il saldo;
#     visualizzare tutte le transazioni;
#     calcolare il totale per categoria;
#     trovare la maggiore uscita;
#     mostrare il numero di entrate e uscite;
#     mostrare il riepilogo;
#     uscire.

# Non accettare importi non positivi,
# impedire spese superiori al saldo,
# usare tuple per le categorie consentite,
# un set per le categorie utilizzate
# e un dizionario per i totali.

# Saldo: 842.30 euro
# Entrate: 1200.00 euro
# Uscite: 357.70 euro

# Totale per categoria:
# - trasporti: 80.00 euro
# - alimentari: 145.20 euro
# - tempo libero: 132.50 euro
# ---------------------------------------------------------

"""
A tuple holds the allowed categories, a set the ones actually used, a
dictionary the totals per category and a list all the transactions, each
stored as a dictionary with type, amount, category and description.
 
Balance, totals, counters and used categories are updated when a
transaction is registered. Amounts must be positive and an expense cannot
exceed the available balance.
 
The largest expense is found by scanning only the transactions of type
"uscita" and keeping the highest amount. A while loop with match handles
the menu, with a separate option for the final summary.
"""
categorie_consentite = (
    "stipendio",
    "trasporti",
    "alimentari",
    "tempo libero",
    "casa",
    "altro"
)

transazioni = []
categorie_utilizzate = set()
totali_categorie = {}
saldo = 0
totale_entrate = 0
totale_uscite = 0
numero_entrate = 0
numero_uscite = 0

while True:
    print("\n--- Portafoglio digitale ---")
    print("1. Registrare un'entrata")
    print("2. Registrare un'uscita")
    print("3. Visualizzare il saldo")
    print("4. Visualizzare tutte le transazioni")
    print("5. Calcolare il totale per categoria")
    print("6. Trovare la maggiore uscita")
    print("7. Mostrare il numero di entrate e uscite")
    print("8. Mostrare il riepilogo")
    print("9. Uscire")

    scelta = input("Scegli un'opzione: ")

    match scelta:

        case "1":
            try:
                importo = float(input("Importo dell'entrata: "))

                if importo <= 0:
                    print("L'importo deve essere positivo")
                    continue

                ricerca = input("Cerca una categoria: ").lower()

                categorie_trovate = []

                for categoria_disponibile in categorie_consentite:
                    if ricerca in categoria_disponibile:
                        categorie_trovate.append(categoria_disponibile)

                if not categorie_trovate:
                    print("Nessuna categoria trovata")
                    continue

                print("\nCategorie trovate:")

                for indice, categoria_trovata in enumerate(
                    categorie_trovate, start=1
                ):
                    print(f"{indice}. {categoria_trovata}")

                try:
                    scelta_categoria = int(
                        input("Scegli una categoria: ")
                    )
                except ValueError:
                    print("Inserisci un numero")
                    continue

                if (
                    scelta_categoria < 1
                    or scelta_categoria > len(categorie_trovate)
                ):
                    print("Scelta non valida")
                    continue

                categoria = categorie_trovate[scelta_categoria - 1]

                descrizione = input("Descrizione: ")

                transazione = {
                    "tipo": "entrata",
                    "importo": importo,
                    "categoria": categoria,
                    "descrizione": descrizione
                }

                transazioni.append(transazione)

                saldo += importo
                totale_entrate += importo
                numero_entrate += 1

                categorie_utilizzate.add(categoria)

                if categoria not in totali_categorie:
                    totali_categorie[categoria] = 0

                totali_categorie[categoria] += importo

                print("Entrata registrata")

            except ValueError:
                print("Inserisci un importo valido")

        case "2":
            try:
                importo = float(input("Importo dell'uscita: "))

                if importo <= 0:
                    print("L'importo deve essere positivo")
                    continue

                if importo > saldo:
                    print("Spesa superiore al saldo disponibile")
                    continue

                ricerca = input("Cerca una categoria: ").lower()

                categorie_trovate = []

                for categoria_disponibile in categorie_consentite:
                    if ricerca in categoria_disponibile:
                        categorie_trovate.append(categoria_disponibile)

                if not categorie_trovate:
                    print("Nessuna categoria trovata")
                    continue

                print("\nCategorie trovate:")

                for indice, categoria_trovata in enumerate(
                    categorie_trovate, start=1
                ):
                    print(f"{indice}. {categoria_trovata}")

                try:
                    scelta_categoria = int(
                        input("Scegli una categoria: ")
                    )
                except ValueError:
                    print("Inserisci un numero")
                    continue

                if (
                    scelta_categoria < 1
                    or scelta_categoria > len(categorie_trovate)
                ):
                    print("Scelta non valida.")
                    continue

                categoria = categorie_trovate[scelta_categoria - 1]

                descrizione = input("Descrizione: ")

                transazione = {
                    "tipo": "uscita",
                    "importo": importo,
                    "categoria": categoria,
                    "descrizione": descrizione
                }

                transazioni.append(transazione)

                saldo -= importo
                totale_uscite += importo
                numero_uscite += 1

                categorie_utilizzate.add(categoria)

                if categoria not in totali_categorie:
                    totali_categorie[categoria] = 0

                totali_categorie[categoria] += importo

                print("Uscita registrata.")

            except ValueError:
                print("Inserisci un importo valido")

        case "3":
            print(f"Saldo: {saldo:.2f} euro")

        case "4":
            if transazioni:
                print("\n--- Transazioni ---")

                for indice, transazione in enumerate(
                    transazioni, start=1
                ):
                    print(
                        f"{indice}. "
                        f"{transazione['tipo']} - "
                        f"{transazione['importo']:.2f} euro - "
                        f"{transazione['categoria']} - "
                        f"{transazione['descrizione']}"
                    )
            else:
                print("Non ci sono transazioni")

        case "5":
            if totali_categorie:
                print("\n--- Totale per categoria ---")

                for categoria, totale in totali_categorie.items():
                    print(
                        f"- {categoria}: "
                        f"{totale:.2f} euro"
                    )
            else:
                print("Non ci sono categorie utilizzate")

        case "6":
            maggiore_uscita = None

            for transazione in transazioni:
                if transazione["tipo"] == "uscita":
                    if (
                        maggiore_uscita is None
                        or transazione["importo"]
                        > maggiore_uscita["importo"]
                    ):
                        maggiore_uscita = transazione

            if maggiore_uscita is not None:
                print("\n--- Maggiore uscita ---")
                print(
                    f"Importo: "
                    f"{maggiore_uscita['importo']:.2f} euro"
                )
                print(
                    f"Categoria: "
                    f"{maggiore_uscita['categoria']}"
                )
                print(
                    f"Descrizione: "
                    f"{maggiore_uscita['descrizione']}"
                )
            else:
                print("Non ci sono uscite.")

        case "7":
            print(f"Numero di entrate: {numero_entrate}")
            print(f"Numero di uscite: {numero_uscite}")

        case "8":
            print("\n--- Riepilogo ---")
            print(f"Saldo: {saldo:.2f} euro")
            print(f"Entrate: {totale_entrate:.2f} euro")
            print(f"Uscite: {totale_uscite:.2f} euro")
            print(f"Numero di entrate: {numero_entrate}")
            print(f"Numero di uscite: {numero_uscite}")

            print("\nCategorie utilizzate:")

            if categorie_utilizzate:
                for categoria in categorie_utilizzate:
                    print(f"- {categoria}")
            else:
                print("Nessuna categoria utilizzata")

        case "9":
            print("Chiusura del portafoglio")
            break

        case _:
            print("Scelta non valida")
