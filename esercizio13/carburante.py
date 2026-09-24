# Crea un file carburante.py in VS Code.

# Il programma deve chiedere:

#     Chilometri percorsi
#     Litri consumati
#     Prezzo di un litro di carburante

# Deve calcolare e stampare:

#     Consumo medio in km/l
#     Costo totale del rifornimento

# Formula
# consumo = chilometri / litri
# costo = litri * prezzo_litro

km = float(input("Inserisci i chilometri percorsi: "))
litri = float(input("Inserisci i litri consumati: "))
prezzo_litro = float(input("Inserisci il prezzo di un litro di carburante: "))

consumo = km / litri
costo = litri * prezzo_litro

print(f"Consumo medio: {consumo} km/l")
print(f"Costo totale del rifornimento: {costo} euro")