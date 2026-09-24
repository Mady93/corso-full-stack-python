# Crea il file temperatura.py.

# Il programma chiede una temperatura con float(input(...)) e stampa:
# Condizione	Messaggio
# temperatura < 0	“Sotto zero”
# temperatura da 0 a 19.9	“Fresco”
# temperatura da 20 a 29.9	“Temperatura gradevole”
# temperatura ≥ 30	“Fa caldo”


temperatura = float(input("Inserisci la temperatura: "))

match temperatura:
    #Prendi val temperatura e dagli un nome es: x, controlla se x < 0
    case x if x < 0:
        print("Sotto zero")
    case x if 0 <= x < 20:
        print("Fresco")
    case x if 20 <= x < 30:
        print("Temperatura gradevole")
    case x if x >= 30:
        print("Fa caldo")
    # Se nessuno dei case precedenti è andato bene, fai questo
    case _:
        print("Valore non valido")


# temperatura =float(input("Temperatura: "))
# if temperatura <= 0:
#     print("Sotto zero")
# elif temperatura <=19.9:
#     print("Fresco")
# elif temperatura <= 29.9:
#     print("Temperatura gradevole")
# else:
#     print("Caldo")




for lettera in "CIAO":
    # non stampa sulla stessa riga:
    # C
    # I
    # A
    # O
    # print(f"{lettera}")

    # stampa sulla stessa riga
    print(lettera, end="") 