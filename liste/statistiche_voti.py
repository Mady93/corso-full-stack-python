# Consegna

# Crea una lista di almeno cinque voti interi. Poi usa un ciclo for per:

# Stampare ogni voto con la sua posizione, usando enumerate(..., start=1).
# Calcolare la somma dei voti con una variabile accumulatore.
# Contare quanti voti sono sufficienti, cioè ≥ 6.
# Alla fine stampa somma e numero di voti sufficienti.

print("\n" + "-" * 60)
voti = [10, 3, 5, 8, 8]

somma = 0
c = 0

for posizione, voto in enumerate(voti, start = 1):
    print(f"Indice {posizione}: Valore {voto}")

    somma += voto

    if voto >= 6:
        c += 1

print(f"Somma: {somma}")
print(f"Voti >= 6: {c}")
print("\n" + "-" * 60)

# Consegna 2 provare a fare la stessa roba anche con i dizionari
grades = {
    "Matematica": [8.5, 7, 9.5, 10, 4.5],
    "Informatica": [10, 9.5, 2, 6.5, 4],
    "Inglese": [7.5, 6, 8.5, 8, 8.5]
}

for index, (materia, voti) in enumerate(grades.items(), start = 1):
    print(f"{index}. {materia}: {voti}")

print("\n" + "-" * 60)

# la media sarà automaticamente float
grades["Matematica"].append(10)
grades["Storia"] = [7]

print("Registro aggiornato: aggiunto il voto 10 in Matematica")
print("Registro aggiornato: aggiunta la materia Storia con voto 7")

print("\n" + "-" * 60)

for index, (materia, voti) in enumerate(grades.items(), start = 1):
    print(f"{index}. {materia}: {voti}")

print("\n" + "-" * 60)

for materia, voti in grades.items():
    media = sum(voti) / len(voti)
    # stampa la media con 2 cifre dopo la virgola
    print(f"{materia}: {media:.2f}")

print("\n" + "-" * 60)
        