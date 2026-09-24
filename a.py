# Input nome dell'utente e saluto personalizzato
nome = input("Come ti chiami? ")
print(f"Ciao, {nome}! Python funziona correttamente.")

nomi_for = ["Alice", "Bob", "Charlie"]

#Stampa i nomi tramite un ciclo foreach
for nome in nomi_for:
    print(f"Ciao, {nome}!")


#Stampa i nomi tramite un ciclo for indicizzato
for i in nomi_for:
    print(f"{i}")


#Stampa i treamite ciclo foreach e contatore
i=0
for c in nomi_for:
    print(f"Indice: {i}")
    i+=1


#Stampa i tramite ciclo foreach e index
for b in nomi_for:
    print(f"{nomi_for.index(b)}")


#Stampa la lunghezza della stringa nome
nome = "Giovanni"
print(f"lunghezza: {len(nome)}")


#Stampa la lunghezza della lista nomi_for
print(f"lunghezza: {len(nomi_for)}")


#Iterazione valori con range che puo essere usato per iterare su una sequenza di numeri interi. range(start, stop, step)
stagioni = ['Primavera', 'Estate', 'Autunno', 'Inverno']
for i in range(len(stagioni)):
   print(stagioni[i]) 


#Stampa nomi con indice
   for i in nomi_for:
     print(f" Champagne per il mio compare {i} in alto il calice {nomi_for.index(i)+1}")
     
