# Scrivere un programma Python che chieda all'utente di inserire un numero intero positivo 
# e calcoli il suo fattoriale utilizzando un ciclo for 

numero = int(input("Inserisci un numero positivo: "))

while numero <= 0:
    numero = int(input("Inserisci un numero valido positivo: "))

count = 1;

for i in range(1, numero + 1):
    count *= i

    print(f"Fattoriale: {count}")


# n = input("Inserisci un numero: ")
# while not numero.isdigit() and not int(numero)<0: 
#     n = input("Non valido. Inserisci un numero: ")