# Crea esercizio9/saluti.py.

# Il programma deve chiedere:

#     Nome della persona
#     Numero di saluti da stampare

# Deve poi stampare il saluto richiesto più volte, usando un ciclo for e range().
# Esempio
# Nome: Anna
# Quanti saluti? 3

# 1. Ciao, Anna!
# 2. Ciao, Anna!
# 3. Ciao, Anna!

# Argomenti già visti
# for numero in range(3):
#     print(numero)

# Adatta questo schema al tuo programma.
# Vincoli

#     Converti il numero inserito con int().
#     Usa range().
#     Usa una f-string nel messaggio.
#     Esegui lo script dal terminale.

nome = input("Nome: ")
numero_saluti = int(input("Quanti saluti? "))

for i in range(numero_saluti):
    print(f"{i + 1}. Ciao, {nome}!")