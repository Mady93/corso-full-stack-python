# Crea un file chiamato conversioni.py.

# Il programma deve chiedere:

#     Nome
#     Numero di ore studiate oggi
#     Numero di minuti aggiuntivi

# Deve convertire ore e minuti in interi, calcolare i minuti totali e stampare una frase personalizzata.
# Esempio atteso
# Nome: Sara
# Ore studiate: 2
# Minuti aggiuntivi: 30

# Sara ha studiato per 150 minuti.

# Suggerimento

# Completa da solo la parte relativa al nome e al messaggio finale con una f-string.

# Esegui il file dal terminale: py conversioni.py su Windows oppure python3 conversioni.py su Linux/macOS.

nome = input("Nome: ")
ore_studiate = int(input("Ore studiate: "))
minuti_aggiuntivi = int(input("Minuti aggiuntivi: "))
tot_min = ore_studiate * 60 + minuti_aggiuntivi

print(f"Nome: {nome} ha studiato per {tot_min} minuti.")


print(f"Le ore studiate in virgola mobile sono: {tot_min / 60}")