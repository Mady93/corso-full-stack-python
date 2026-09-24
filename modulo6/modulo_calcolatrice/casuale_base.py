# Attività»» 3 — Script casuale base Autonoma
# Consegna

# Crea casuale_base.py. Il programma deve:

#     Importare il modulo random.
#     Generare un numero casuale tra 1 e 100.
#     Chiedere all'utente di indovinare il numero.
#     Stampare se il tentativo è troppo alto, troppo basso o corretto.

# Esempio
# Ho pensato un numero tra 1 e 100.
# Tuo tentativo: 50
# Troppo basso!
# Tuo tentativo: 75
# Troppo alto!
# Tuo tentativo: 63
# Hai indovinato!

import random
 
segreto = random.randint(1, 100)
print("Ho pensato un numero tra 1 e 100.")
 
while True:
    tentativo = int(input("Tuo tentativo: "))
    if tentativo < segreto:
        print("Troppo basso!")
    elif tentativo > segreto:
        print("Troppo alto!")
    else:
        print("Hai indovinato!")
        break
