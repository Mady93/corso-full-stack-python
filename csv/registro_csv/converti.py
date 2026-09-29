import csv    # per leggere il file CSV
import json   # per scrivere il file JSON

# Apro il CSV in lettura ("r"). newline="" è il parametro consigliato per i CSV.
with open("registro.csv", "r", newline="", encoding="utf-8") as file:
    # DictReader trasforma ogni riga in un dizionario: le chiavi sono i nomi
    # della prima riga (nome, cognome, eta, citta).
    # list(...) mette tutti i dizionari in una lista, così i dati restano
    # disponibili anche dopo la chiusura del file da parte del "with".
    record = list(csv.DictReader(file))

# il CSV legge tutto come stringa: l'età la riportiamo a numero
# Passo in rassegna ogni persona e converto '33' (testo) in 33 (numero).
# Nel JSON finale l'età sarà quindi senza virgolette.
for r in record:
    r["eta"] = int(r["eta"])

# Apro il JSON in scrittura ("w"): se esiste già, lo sovrascrive.
with open("registro.json", "w", encoding="utf-8") as file:
    # json.dump scrive la lista Python nel file in formato JSON.
    # ensure_ascii=False -> mantiene le lettere accentate (à, è...) leggibili
    # indent=4           -> va a capo e indenta, così il file è leggibile
    json.dump(record, file, ensure_ascii=False, indent=4)

# Messaggio finale, solo per sapere che la conversione è andata a buon fine.
print("Convertito in registro.json")