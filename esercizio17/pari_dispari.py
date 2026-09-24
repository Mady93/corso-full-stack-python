# Consegna

# Crea pari_dispari.py.

# Il programma deve:

#     Chiedere un limite intero positivo.
#     Usare for e range() per esaminare i numeri da 1 al limite.
#     Usare continue per saltare i numeri dispari.
#     Stampare solo i numeri pari.
#     Interrompere il ciclo con break quando raggiunge il primo numero pari maggiore di 20.

limite = int(input("Inserisci un intero positivo: "))
for i in range(1, limite +1):

    if i % 2 != 0:
        continue
    print(f"Pari: {i}", end=" ")

    if i > 20:
        break