# Crea esercizio8/calcolatrice.py.

# Il programma deve:

#     Chiedere due numeri interi.
#     Calcolare somma, differenza (se possibile) prodotto e divisione (con resto)
#     Stampare i risultati con messaggi chiari.

# Esempio
# Primo numero: 8
# Secondo numero: 3

# Somma: 11
# Differenza: 5
# Prodotto: 24

a = int(input("Primo numero: "))
b = int(input("Secondo numero: "))

print(f"Somma: {a + b}")
print(f"Differenza: {a - b}")
print(f"Prodotto: {a * b}")
print(f"Divisione: {a // b} con resto {a % b}")