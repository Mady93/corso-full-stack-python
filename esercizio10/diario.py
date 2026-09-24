# Scenario

# Devi realizzare un piccolo progetto Python che raccolga informazioni su un'attività di laboratorio.
# Consegna

# Crea questa struttura:
# esercizio10/
# ├── diario.py
# └── appunti/

# Il file diario.py deve chiedere:

#     Nome dello studente
#     Nome dell'attività
#     Numero di minuti impiegati
#     Quante volte desidera stampare il riepilogo

# Output richiesto

# Il programma deve usare un ciclo for e stampare un riepilogo numerato:
# Riepilogo 1: Luca ha svolto "Primo script" in 30 minuti.
# Riepilogo 2: Luca ha svolto "Primo script" in 30 minuti.
# Vincoli

#     Trasforma minuti e ripetizioni in interi con int().
#     Usa almeno quattro input().
#     Usa almeno una f-string.
#     Usa un ciclo for con range().
#     Prima di eseguire, mostra struttura e posizione con pwd e ls -la.
#     Dopo la prova, rimuovi solo la cartella appunti se è vuota, senza eliminare diario.py.

nome_studente = input("Nome dello studente: ")
nome_attivita = input("Nome dell'attività: ")
minuti = int(input("Numero di minuti impiegati: "))
ripetizioni = int(input("Quante volte desidera stampare il riepilogo?"))

for i in range(1, ripetizioni + 1):
    print(f"Riepilogo {i}: {nome_studente} ha svolto \"{nome_attivita}\" in {minuti} minuti.")
