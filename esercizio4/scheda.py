# Crea la cartella esercizio4. Al suo interno crea il file scheda.py.

# Il programma deve chiedere:

#     Nome
#     Città
#     Colore preferito

# Deve stampare un messaggio personalizzato usando una f-string.

# Esempio
# Come ti chiami? Sara
# In quale città vivi? Palermo
# Colore preferito? Blu

# Sara vive a Palermo e preferisce il blu.

# Vincoli

#     Usa tre input().
#     Usa almeno una f-string.
#     Controlla con ls che il file esista.
#     Esegui il file dal terminale.
#     Non usare il pulsante ▶ come unico metodo di esecuzione.

# Non sono forniti i passaggi: devi scegliere autonomamente i comandi di navigazione e creazione cartelle.


nome = input("Come ti chiami? ")
citta = input("In quale città vivi?")
colore_preferito = input("Colore preferito?")

print(f"{nome} vive a {citta} e preferisce il {colore_preferito}.")