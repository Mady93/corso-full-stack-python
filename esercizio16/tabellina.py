# Crea il file tabellina.py.

# Il programma deve:

#     Chiedere un numero intero.
#     Verificare il numero inserito
#     Usare un ciclo for e range().
#     Stampare la tabellina da 1 a 10.

# Esempio
# Numero: 7
# 7 x 1 = 7
# 7 x 2 = 14
# ...
# 7 x 10 = 70

n = int(input("Inserisci un numero: "))

# if(type(n)==int):
if isinstance(n, int):
    print("n è un intero")

    for i in range(1, 11):
        val = n * i

        print(f"{val}")

#Pass si usa per funzioni con logica ancora non completata
if n > 10:
    pass
else:
    print("Numero piccolo")

#Break esce fuori dal ciclo
for riga in range(1, 4):
    for colonna in range(1, 4):
        if colonna == 2:
            break
        print(f"Riga {riga}, colonna {colonna}") 

#Continue salta la condizione stessa


#quando colonna è diverso da 3 stampo end finale
for riga in range(1, 4):

    for colonna in range(1, 4):
        if colonna != 3:
            print(f"[Riga {riga}, colonna {colonna}]", end=" ") 

        else:
            print(f"[Riga {riga}, colonna {colonna}]") 
