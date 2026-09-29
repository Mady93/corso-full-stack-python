import csv
import json
import os

FILE_CSV = "registro.csv"      # 1) file usato solo per la conversione
FILE_JSON = "registro.json"    # 1) nuovo file dati


def file_vuoto():
    """True se il JSON non esiste o non contiene nulla."""
    # os.path.exists  -> controlla se il file c'è sul disco
    # os.path.getsize -> dimensione in byte (0 = file creato ma senza nulla dentro)
    # "not exists OR size == 0": basta una delle due condizioni per dire "vuoto".
    # Se il file non esiste, l'"or" si ferma subito e getsize non viene chiamata
    # (altrimenti darebbe errore su un file inesistente).
    return not os.path.exists(FILE_JSON) or os.path.getsize(FILE_JSON) == 0


def leggi_record():
    """Restituisce tutti i record come lista di dizionari."""
    # Se il file non c'è o è vuoto restituisco una lista vuota, così il resto
    # del programma non va in errore (FileNotFoundError) alla prima esecuzione.
    if file_vuoto():
        return []
    # Modalità "r": apro il file solo in lettura.
    with open(FILE_JSON, "r", encoding="utf-8") as file:
        # json.load legge il file e lo trasforma direttamente in oggetti Python:
        # qui ottengo una lista di dizionari, uno per persona.
        # L'età torna un numero (int) perché nel JSON è salvata senza virgolette.
        return json.load(file)


def salva_record(record):
    """Riscrive l'intero file JSON con la lista di record."""
    # Modalità "w": cancella il vecchio contenuto e riscrive tutto da capo.
    # Con il JSON non posso aggiungere una riga in fondo come nel CSV con "a",
    # perché il file è un'unica lista [ ... ]: devo riscriverla intera.
    with open(FILE_JSON, "w", encoding="utf-8") as file:
        # json.dump fa l'opposto di json.load: scrive la lista Python nel file.
        # ensure_ascii=False -> mantiene le lettere accentate (à, è...) leggibili
        # indent=4           -> va a capo e indenta, così il file è leggibile
        json.dump(record, file, ensure_ascii=False, indent=4)


# 2)Conversione automatica
def converti_csv_in_json():
    """Se esiste il CSV e il JSON è vuoto, converte automaticamente."""
    # Esco subito (return) in due casi, senza fare nulla:
    #  - il CSV non esiste  -> non c'è niente da convertire
    #  - il JSON ha già dati -> non devo sovrascriverlo
    # Quindi la conversione avviene solo una volta, alla prima esecuzione.
    if not os.path.exists(FILE_CSV) or not file_vuoto():
        return

    # newline="" è il parametro consigliato per i file CSV.
    with open(FILE_CSV, "r", newline="", encoding="utf-8") as file:
        # DictReader legge ogni riga come dizionario (chiavi = intestazione).
        # list(...) trasforma il risultato in una lista, così posso usarlo
        # anche dopo che il file è stato chiuso dal "with".
        record = list(csv.DictReader(file))

    # Il CSV restituisce sempre stringhe ('33'), quindi riconverto l'età in
    # numero (33) prima di salvare. Uso isdigit() per evitare errori se in
    # qualche riga l'età fosse vuota o scritta male.
    for r in record:
        if str(r["eta"]).isdigit():
            r["eta"] = int(r["eta"])

    # Riuso salva_record: scrive la lista convertita nel file JSON.
    salva_record(record)
    print(f"Ho convertito {len(record)} record da {FILE_CSV} a {FILE_JSON}.")


def inserisci():
    nome = input("Nome: ").strip()
    cognome = input("Cognome: ").strip()

    while True:
        eta = input("Età: ").strip()
        if eta.isdigit():
            break
        print("Inserisci un numero intero.")

    citta = input("Città: ").strip()

    persona = {"nome": nome, "cognome": cognome, "eta": int(eta), "citta": citta}

    record = leggi_record()   # leggo tutto
    record.append(persona)    # aggiungo in memoria
    salva_record(record)      # riscrivo tutto il file

    print("Record salvato.")


def stampa_record(record):
    # Stampa una sola persona su una riga, con le colonne allineate.
    # Nelle f-string, {campo:<12} significa "allinea a sinistra in 12 caratteri":
    # così le colonne restano incolonnate anche con nomi di lunghezza diversa.
    print(f"{record['nome']:<12} {record['cognome']:<12} "
          f"{record['eta']:<4} {record['citta']}")


def visualizza():
    record = leggi_record()
    # Lista vuota = "falsa" in Python, quindi "not record" vuol dire "nessun record".
    if not record:
        print("Il registro è vuoto.")
        return
    # Intestazione della tabella, con la stessa larghezza delle colonne di sotto.
    print(f"\n{'NOME':<12} {'COGNOME':<12} {'ETÀ':<4} CITTÀ")
    print("-" * 40)   # riga di trattini lunga 40 caratteri
    # Per ogni persona chiamo stampa_record, così non ripeto il formato qui.
    for r in record:
        stampa_record(r)
    print(f"\nTotale: {len(record)} persone")


def cerca():
    # .lower() e .strip(): ignoro maiuscole/minuscole e spazi inutili.
    cognome = input("Cognome da cercare: ").strip().lower()
    # List comprehension: tiene solo i record in cui il testo digitato è
    # contenuto ("in") nel cognome, anch'esso in minuscolo.
    # Quindi cercando "p" trovo tutti i cognomi che contengono una "p".
    trovati = [r for r in leggi_record() if cognome in r["cognome"].lower()]

    # Lista vuota = nessuna corrispondenza.
    if not trovati:
        print("Nessuna persona trovata.")
        return
    print(f"\n{'NOME':<12} {'COGNOME':<12} {'ETÀ':<4} CITTÀ")
    print("-" * 40)
    for r in trovati:
        stampa_record(r)


def main():
    converti_csv_in_json()   # 3) chiamata automatica all'avvio

    # Il menu si ripete all'infinito finché non si sceglie 0 (break).
    while True:
        print("\n=== REGISTRO PERSONE ===")
        print("1) Inserisci nuova persona")
        print("2) Visualizza tutte le persone")
        print("3) Cerca per cognome")
        print("0) Esci")
        scelta = input("Scelta: ").strip()

        if scelta == "1":
            inserisci()
        elif scelta == "2":
            visualizza()
        elif scelta == "3":
            cerca()
        elif scelta == "0":
            print("Arrivederci!")
            break
        else:
            print("Scelta non valida")


# Questo blocco fa partire main() solo se il file viene eseguito direttamente
# (python registro.py). Se il file fosse importato da un altro, non partirebbe.
if __name__ == "__main__":
    main()