# Attività»» 5 — Script che usa utility_casuali Autonoma
# Consegna

# Crea gioco_casuale.py. Il programma deve:

#     Importare utility_casuali.
#     Chiedere all'utente se vuole lanciare un dado o estrarre un nome.
#     Se dado: chiamare lancia_dado() e stampare il risultato.
#     Se nome: definire una lista di nomi, chiamare estrai_nome(nomi) e stampare il nome scelto.
#     Prima di giocare, chiedere la password di autenticazione (max 3 tentativi) 

import utility_casuali
 
PASSWORD_CORRETTA = "python123"
MAX_TENTATIVI = 3
 
# Autenticazione: massimo 3 tentativi
autenticato = False

# Ripeto la richiesta della password al massimo 3 volte (tentativo vale 1, 2, 3)
for tentativo in range(1, MAX_TENTATIVI + 1):
    password = input("Password di autenticazione: ")

    # Se la password è giusta, segno l'accesso e interrompo il ciclo con break
    if password == PASSWORD_CORRETTA:
        autenticato = True
        break
    # Password sbagliata: dico quanti tentativi rimangono
    print(f"Password errata. Tentativi rimasti: {MAX_TENTATIVI - tentativo}")

 # Se dopo i tentativi non sono autenticato, blocco il programma
if not autenticato:
    print("Accesso negato")
else:
    print("Accesso consentito!")

    # strip() toglie gli spazi e lower() mette in minuscolo, così "Dado " funziona
    scelta = input("Vuoi lanciare un dado o estrarre un nome? (dado/nome): ").strip().lower()
 
    if scelta == "dado":

        # Chiamo la funzione del modulo e stampo il valore restituito
        risultato = utility_casuali.lancia_dado()
        print(f"Hai ottenuto: {risultato}")

    elif scelta == "nome":

        # Definisco la lista di nomi tra cui estrarre
        nomi = ["Anna", "Luca", "Giulia", "Marco", "Sara"]
        estratto = utility_casuali.estrai_nome(nomi)
        print(f"Nome estratto: {estratto}")
    else:
        # Né "dado" né "nome": avviso l'utente
        print("Scelta non valida. Scrivi 'dado' oppure 'nome'")
